from OnlineSoccerManagerBot.service import OnlineSoccerManagerService

class OnlineSoccerManagerController:

    #instantiate the service
    def __init__(self):
        self.manager = OnlineSoccerManagerService()

    # call service get token function
    def getTokens(self):
        self.manager.get_business_tokens()
