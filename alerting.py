import os
import subprocess
import discord_webhook
import time
import sys

CHECK_FREQ = 30  # Every 60 seconds
if len(sys.argv) > 1 and sys.argv[1].isnumeric():
    CHECK_FREQ = int(sys.argv[1])

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/877623688034414623/ZtJ0nx6gTNzc_gOpSq67cH1wqVZwLMR5B5xDfFc4IsarexAhOUxJZFdvBgfbjyc-nco_"

COMMANDS = (
    "systemctl status gtoplus.service",
    "systemctl status mongod.service",
    "systemctl status postgresql.service",
)

SERVICES = (
    "GTO Plus",
    "MongoDB",
    "PostgreSQL"
)


def check_service(service_number: int):
    try:
        res = subprocess.check_output(
            [*COMMANDS[service_number].split(" ")]).decode().split("\n")[2]
        if "active" not in res:
            print("{} not running".format(SERVICES[service_number]))
            webhook = discord_webhook.DiscordEmbed(url=DISCORD_WEBHOOK, content="\n".join(
                [res, "**{} not running**".format(SERVICES[service_number])]))
            webhook.execute()
    except subprocess.CalledProcessError as e:
        print("{} not running".format(SERVICES[service_number]))
        webhook = discord_webhook.DiscordWebhook(url=DISCORD_WEBHOOK, content="\n".join(
            ["**{} not running**".format(SERVICES[service_number]), "{}".format(e)]))
        webhook.execute()


if __name__ == '__main__':
    print("Running alerting script")
    while True:
        check_service(0)
        check_service(1)
        check_service(2)
        time.sleep(CHECK_FREQ)
