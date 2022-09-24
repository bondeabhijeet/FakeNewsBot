


def BotHelpMessage(Commands):
    print(Commands)

    Msg = f"""
/{Commands['Help']}
>> Will get this message.

/{Commands['News']} <code>[ News ]</code> 
>> Will predict whether the news is real or fake.
"""

    print("Help requested!!!")
    return Msg