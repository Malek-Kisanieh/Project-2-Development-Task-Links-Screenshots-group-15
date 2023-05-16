##################Main_client######################
def main():
    SERVER = 'ev3dev'

    client = BluetoothMailboxClient()
    mbox = TextMailbox('greeting', client)
    print('establishing connection...')
    client.connect(SERVER)
    print('connected!')

    start_position, start_height, d, d2 = parameters()
    ev3.screen.clear()
    calibrate(-330,120)
    mbox.send('hello!')
    

    run=True
    delivered=False
    while run:
        mbox.wait()
        if mbox.read()=="delivered":
            calibrate(start_position,start_height)
            grab()
            color_brick=rgb_sensor()
            if color_brick not in d.keys():
                ev3.speaker.say("I dont have a drop off zone for that color")
            elif "all" in d.keys():
                all_colors_p = d.get("all")
                axis.run_target(60,all_colors_p)
            try:
                end_position = d.get(color_brick)
                end_height = d2.get(color_brick)
                axis.run_target(60,end_position)
                elbow.run_target(60,end_height)
                delivered=True
                run=False
            except:
                pass
            restart(start_position,start_height)
    if delivered:
        calibrate(-330,120)
        mbox.send("delivered")
        delivered=False
        run=True

main()
############################################
