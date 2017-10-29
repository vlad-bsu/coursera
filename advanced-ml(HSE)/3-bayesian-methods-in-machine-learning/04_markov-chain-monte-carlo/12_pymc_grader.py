import requests
import json
import numpy as np
from collections import OrderedDict

class Grader(object):
    def __init__(self):
        self.submission_page = 'https://www.coursera.org/api/onDemandProgrammingScriptSubmissions.v1'
        self.assignment_key = 'u85FqY8sEee5cg635EOBeA'
        self.parts = OrderedDict([
                      ('pn017', '1.1 (Alice trajectory)'),
                      ('UUbsF', '1.1 (Bob trajectory)'),
                      ('FFmXD', '1.2 (Alice mean)'), 
                      ('uWPFR', '1.2 (Bob mean)'), 
                      ('nkkem', '1.3'), 
                      ('dyuVW', '1.4')
                      ])
        self.answers = {key: None for key in self.parts}

    @staticmethod
    def ravel_output(output):
        '''
           If student accedentally submitted np.array with one
           element instead of number, this function will submit
           this number instead
        '''
        if isinstance(output, np.ndarray) and output.size == 1:
            output = output.item(0)
        return output

    def submit(self, email, token):
        submission = {
                    "assignmentKey": self.assignment_key, 
                    "submitterEmail": email, 
                    "secret": token, 
                    "parts": {}
                  }
        for part, output in self.answers.items():
            if output is not None:
                submission["parts"][part] = {"output": output}
            else:
                submission["parts"][part] = dict()
        request = requests.post(self.submission_page, data=json.dumps(submission))
        response = request.json()
        if request.status_code == 201:
            print('Submitted to Coursera platform. See results on assignment page!')
        elif u'details' in response and u'learnerMessage' in response[u'details']:
            print(response[u'details'][u'learnerMessage'])
        else:
            print("Unknown response from Coursera: {}".format(request.status_code))
            print(response)

    def status(self):
        print("You want to submit these numbers:")
        for part_id, part_name in self.parts.items():
            answer = self.answers[part_id]
            if answer is None:
                answer = '-'*10
            print("Task {}: {}".format(part_name, answer))
               
    def submit_part(self, part, output):
        self.answers[part] = output
        print("Current answer for task {} is: {}".format(self.parts[part], output))

    def submit_simulation_trajectory(self, alice_trajectory, bob_trajectory):
        self.submit_part('pn017', '{}  {}'.format(
            self.ravel_output(alice_trajectory[0]), self.ravel_output(alice_trajectory[1])
            ))
        self.submit_part('UUbsF', '{}  {}'.format(
            self.ravel_output(bob_trajectory[0]), self.ravel_output(bob_trajectory[1])
            ))
    
    def submit_simulation_mean(self, alice_price, bob_price):
        self.submit_part('FFmXD', str(self.ravel_output(alice_price)))
        self.submit_part('uWPFR', str(self.ravel_output(bob_price)))
    
    def submit_simulation_correlation(self, alice_bob_correlation):
        self.submit_part('nkkem', str(self.ravel_output(alice_bob_correlation)))
    
    def submit_simulation_depends(self, answer):
        self.submit_part('dyuVW', answer)
    

    