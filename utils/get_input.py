import random

class getUserItem(object):
    def __init__(self, data):
        self.uid = None
        self.iid = None
        self.data = data
        self.user_id_list = list(self.data.user_id2org.keys())
        self.sorted_preferences = self.get_sorted_preferences()
    
    def get_sorted_preferences(self):
        user_preferences = self.data.kg_train_data[self.data.kg_train_data.r == 0].groupby('h')['t'].count()
        sorted_preferences = user_preferences.sort_values(ascending=False)
        return sorted_preferences.to_frame().reset_index().rename(columns={"h":"uid", "t":"num_items"})
    
    def set_uid(self, is_cold_start=False, uid=None):
        if is_cold_start:
            if uid == None:
                raise Exception("uid is required!")
            self.uid = uid
        else:
            self.uid = random.choice(self.user_id_list)
    
    def set_iid(self):
        if self.uid == None:
            raise Exception("Run set_uid()")
        user_preference_list = self.data.train_kg_dict[self.uid]
        self.iid = random.choice(user_preference_list)[0]
    
    def get_uid(self):
        if self.uid == None:
            raise Exception("Run set_uid()")
        return self.uid
    
    def get_iid(self):
        if self.iid == None:
            raise Exception("Run set_iid()")
        return self.iid
    
    def get_cold_start_uid(self, number_of_interations):
        cold_start_uid_list = list(self.sorted_preferences[self.sorted_preferences.num_items==number_of_interations].uid)
        return cold_start_uid_list