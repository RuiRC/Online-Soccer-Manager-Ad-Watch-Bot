from OnlineSoccerManagerBot.controller import OnlineSoccerManagerController

#main function
def main():
    # instantiate the controller
    manager = OnlineSoccerManagerController()
    # call the controller function
    manager.getTokens()


if __name__ == "__main__":
    main()

