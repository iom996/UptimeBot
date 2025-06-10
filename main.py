from aiogram import Bot, Dispatcher
import asyncio
import configparser


config = configparser.ConfigParser()
config.read("../../config.ini")

TOKEN = config["token"]["token"]

dp = Dispatcher()
