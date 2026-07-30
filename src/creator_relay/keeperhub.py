"""Fail-closed KeeperHub direct-execution adapter for testnet reward receipts."""

from __future__ import annotations

import json
import os
import re
import uuid
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Callable
from urllib.request import Request, urlopen


TESTNET_CHAIN_IDS = frozenset({11155111, 84532})  # Ethereum Sepolia, Base Sepolia
ADDRESS = re.compile(r"^0x[a-fA-F0-9]{40}$")


class KeeperHubConfigurationError(ValueError):
    """Raised before a request when owner-controlled config is absent or unsafe."""


@dataclass(frozen=True)
class ExecutionReceipt:
    execution_id: str | None
    status: str
    chain_id: int
    recipient: str
    amount: str
    simulated: bool
    transaction_hash: str | None = None
    transaction_link: str | None = None


class KeeperHubClient:
    """Minimal implementation of KeeperHub's documented Direct Execution API."""

    base_url = "https://app.keeperhub.com/api"

    def __init__(self, api_key: str, request_fn: Callable[..., dict[str, Any]] | None = None):
        if not api_key.startswith("kh_"):
            raise KeeperHubConfigurationError("KEEPERHUB_API_KEY must be a kh_ organization key")
        self.api_key = api_key
        self._request_fn = request_fn or self._http_request

    @classmethod
    def from_environment(cls) -> "KeeperHubClient":
        api_key = os.getenv("KEEPERHUB_API_KEY", "").strip()
        if not api_key:
            raise KeeperHubConfigurationError("KEEPERHUB_API_KEY is required before any KeeperHub request")
        return cls(api_key)

    @staticmethod
    def _validate(chain_id: int, recipient: str, amount: str) -> None:
        if chain_id not in TESTNET_CHAIN_IDS:
            raise ValueError("only supported testnet chain IDs are permitted")
        if not ADDRESS.fullmatch(recipient):
            raise ValueError("recipient must be a 0x-prefixed 20-byte EVM address")
        try:
            parsed = Decimal(amount)
        except InvalidOperation as exc:
            raise ValueError("amount must be a decimal string") from exc
        if not parsed.is_finite() or parsed <= 0:
            raise ValueError("amount must be greater than zero")

    def simulate_transfer(self, *, chain_id: int, recipient: str, amount: str) -> ExecutionReceipt:
        self._validate(chain_id, recipient, amount)
        response = self._request_fn(
            path="/execute/transfer",
            payload={
                "chainId": chain_id,
                "recipientAddress": recipient,
                "amount": amount,
                "simulate": True,
            },
            idempotency_key=None,
        )
        if response.get("success") is not True or response.get("wouldRevert") is not False:
            raise RuntimeError("KeeperHub simulation did not prove this transfer is safe to broadcast")
        return ExecutionReceipt(
            execution_id=None,
            status=str(response.get("status", "simulated")),
            chain_id=chain_id,
            recipient=recipient,
            amount=amount,
            simulated=True,
        )

    def broadcast_testnet_transfer(
        self, *, chain_id: int, recipient: str, amount: str, confirm: bool
    ) -> ExecutionReceipt:
        self._validate(chain_id, recipient, amount)
        if not confirm:
            raise ValueError("refusing broadcast without explicit confirmation")
        response = self._request_fn(
            path="/execute/transfer",
            payload={"chainId": chain_id, "recipientAddress": recipient, "amount": amount},
            idempotency_key=str(uuid.uuid4()),
        )
        return ExecutionReceipt(
            execution_id=response.get("executionId"),
            status=str(response.get("status", "unknown")),
            chain_id=chain_id,
            recipient=recipient,
            amount=amount,
            simulated=False,
        )

    def _http_request(self, *, path: str, payload: dict[str, Any], idempotency_key: str | None) -> dict[str, Any]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        request = Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urlopen(request, timeout=30) as response:  # nosec: owner supplies allowlisted endpoint only
            body = json.loads(response.read().decode("utf-8"))
        return body.get("data", body)
