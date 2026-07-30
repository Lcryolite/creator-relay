"""Local developer entry point."""

from __future__ import annotations

import argparse

from .delivery import SmtpConfig, send_smtp
from .keeperhub import KeeperHubClient, KeeperHubConfigurationError
from .relay import CreatorBrief, MindRelay, channels
from .web import create_app


def main() -> None:
    parser = argparse.ArgumentParser(prog="creator-relay")
    subcommands = parser.add_subparsers(dest="command")
    subcommands.add_parser("serve", help="run the loopback-only local demo")
    send = subcommands.add_parser("send-mind-brief", help="send one real Mind email")
    send.add_argument("--confirm-live-delivery", action="store_true")
    send.add_argument("--mind-id", required=True)
    send.add_argument("--mind-email", required=True)
    send.add_argument("--source", required=True)
    send.add_argument("--audience", required=True)
    send.add_argument("--goal", required=True)
    send.add_argument("--channels", required=True, help="comma-separated channel list")
    keeper = subcommands.add_parser("simulate-community-reward", help="simulate a KeeperHub testnet receipt")
    keeper.add_argument("--chain-id", type=int, default=11155111)
    keeper.add_argument("--recipient", required=True)
    keeper.add_argument("--amount", required=True)
    args = parser.parse_args()

    if args.command in (None, "serve"):
        create_app().run(host="127.0.0.1", port=8790, debug=False)
        return
    if args.command == "simulate-community-reward":
        try:
            receipt = KeeperHubClient.from_environment().simulate_transfer(
                chain_id=args.chain_id, recipient=args.recipient, amount=args.amount
            )
        except (KeeperHubConfigurationError, ValueError) as exc:
            parser.error(str(exc))
        print(receipt)
        return
    if not args.confirm_live_delivery:
        parser.error("refusing live delivery without --confirm-live-delivery")

    brief = CreatorBrief(
        source=args.source,
        audience=args.audience,
        goal=args.goal,
        channels=channels(args.channels.split(",")),
    )
    message = MindRelay(args.mind_email, args.mind_id).compose(brief)
    try:
        config = SmtpConfig.from_environment()
    except ValueError as exc:
        parser.error(str(exc))
    send_smtp(message, config)
