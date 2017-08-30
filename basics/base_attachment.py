from db.db import BaseModel


class BaseAttachment(BaseModel):

    character = False
    action_matrix = False

    def __getstate__(self):
        result = self.__dict__.copy()
        del result['action_matrix']
        return result

    def __setstate__(self, this_dict):
        self.__init__(this_dict['character'])

        this_dict['action_matrix'] = self.action_matrix
        self.__dict__ = this_dict

