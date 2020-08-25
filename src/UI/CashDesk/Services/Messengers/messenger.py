from Handlers.network_handler import NetworkHandler
import Templates.references as REFS

class Messenger():
    def __init__(self, service):
        self.service = service
        self.identifier = service.__class__.__name__

        NetworkHandler.on_message_received_event.add(self.check_incoming_message)

    @staticmethod
    def attach_service_id(service_id, message) -> str:
        return f"{service_id}{REFS.LIST_DELIMITER}{message}"

    @staticmethod
    def process_message(message):
        print("Processing message skipped..")

    def check_incoming_message(self, message):
        ID,BODY = NetworkHandler.get_message_components(message)
        print("Got the following message to check:", ID, BODY)

        service_id = BODY.split(REFS.LIST_DELIMITER)[0]

        if service_id == self.identifier:
            return self.service.process_message(BODY.split(REFS.LIST_DELIMITER)[1])

        return ""