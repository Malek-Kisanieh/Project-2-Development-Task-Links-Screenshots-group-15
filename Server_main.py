##################Main_server######################
def main():
    server = BluetoothMailboxServer()
    mbox = TextMailbox('greeting', server)
    print('waiting for connection...')
    server.wait_for_connection()
    print('connected!')
    calibrate(-330,120)
    mbox.wait()
    print(mbox.read())

    start_position, start_height, d, d2 = parameters()
    ev3.screen.clear()

    run=True
    delivered=False
    while run:
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
           elbow.run_target(60, end_height)
           delivered = True
           run=False
        except:
            pass
        restart(start_position,start_height)
    if delivered:
        calibrate(-330,120)
        mbox.send("delivered")
        mbox.wait()
        if mbox.read()=="delivered":
            delivered=False
            run=True
main()
############################################
