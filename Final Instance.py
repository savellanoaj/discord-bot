'''Importing class libraries to interact with discord, interact with the operating system,
randomly generate something, retrieve metadata from an EC2 instance, and importing the token file''' 
import discord
import os 
import random 
from ec2_metadata import ec2_metadata
from dotenv import load_dotenv


#Loads the environment variable of the token from the .env file
load_dotenv() 

#Create a Discord bot instance pulling the token
client = discord.Bot() 
token = os.getenv('TOKEN')


#When code is run, this event executes and prints the statements when the bot is successfully activated
@client.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(client))
    print(f'EC2 Region: {ec2_metadata.region}')
    print(f'EC2 Instance ID: {ec2_metadata.instance_id}')
    print(f'Public IP Address: {ec2_metadata.public_ipv4}')


'''This event is executed when a message is recieved and will pass information from the received message
which needs to be processed first'''
@client.event 
async def on_message(message): 
    #Converts the objects into strings
    #Indexing and splitting the username because of its #
    username = str(message.author).split("#")[0] 
    channel = str(message.channel.name) 
    user_message = str(message.content) 

    #Prints the information about the received message
    print(f'Message {user_message} by {username} on {channel}') 

    #Ignores the messages sent by the bot itself
    if message.author == client.user: 
        return

    '''If the channel name is random it will run more conditional statements that will check the
    string indexes and lower case the values of the users messages'''
    if channel == "random":

        #try-except block to handle any exceptions from user_message
        try: 

            #Nested if statements to respond to certain messages
            if user_message.lower() == "hello" or user_message.lower() == "hi": 
                await message.channel.send(f'Hello {username}') 
                return#returns the values that are passed into the function

            #Other string option
            elif user_message.lower() == "bye": 
                await message.channel.send(f'Bye {username}') 

            #Returns instance data as the last conditional
            elif user_message.lower() == "tell me about my server":
                await message.channel.send(f'EC2 Region: {ec2_metadata.region}\nEC2 Instance ID: {ec2_metadata.instance_id}\nIP Address: {ec2_metadata.public_ipv4}')

        #Handles any exceptions and reports an error message
        except Exception as e:
            await message.channel.send(f"An error has occurred: {e}")

#Run the bot with the provided token
client.run(token)