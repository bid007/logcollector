#Author : Bidhya Nandan Sharma
#Date 12/18/2017
class RuleMatcher(object):
    """
    Takes log and alert rule as instantition input
    Apply the alert rules to the log and return if something matches
    """
    def __init__(self, log, alert_rules):
        self.log = log
        self.matched = False
        self.msg = []
        try:
            self.match(log, alert_rules)
        except Exception as e:
            print(e)
            print("Could not match rule against log")

    def match(self, log, alert_rules):
        r_msg = []
        #breaks the log into list
        log_list = log.split(" ")
        for alert in alert_rules:
            #gets the type and limit value from alert rule
            a_type = alert['type']+":"
            a_limit = alert['limit']
            #checks if type is in log or not
            if a_type in log_list:

                #finds the index of the type 
                a_type_index = log_list.index(a_type)

                #gets the limit in the log for that type
                log_limit = log_list[a_type_index + 1]

                #removes % and convert to float for comparision 
                log_limit_value = float(log_limit.split("%")[0])
                a_limit_value = float(a_limit.split("%")[0])
                #check if limit is reached or crossed
                if log_limit_value - a_limit_value >= 0:

                    #raise the flag of matched
                    self.matched = True

                    #create a message to be sent as email
                    r_msg.append("Alert for "+ a_type + " limit : "+ log_limit)

        #assign the message to msg property
        self.msg = "\n".join(r_msg)

#doing test####
# alert_rule = [{'type':'cpu', 'limit':'0%'},{'type':'memory', 'limit':'0%'}]
# log = 'memory: 0.07%, cpu: 0.39%'
# r = RuleMatcher(log, alert_rule)
# print(r.matched)
# print(r.msg)
# r = RuleMatcher("adfadf",alert_rule)
