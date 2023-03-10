from http.server import BaseHTTPRequestHandler, HTTPServer
from jsonrpclib import Server
import time
import threading
import cgi
import random
import jooble_api

class Sender(threading.Thread):
    
    def __init__(self, thread_name, chanel_name, full_thread_name, nb_of_message_2_send, message_type, game_id):
        print("Server has started!")
        threading.Thread.__init__(self, name=full_thread_name)
        self.thread_name = thread_name
        self.chanel_name = chanel_name
        self.full_thread_name = full_thread_name
        self.broker = Server('http://localhost:1006')
        self.nb_of_message_2_send = nb_of_message_2_send
        self.message_type = message_type
        self.game_id = game_id

    def run(self):
        print(self.full_thread_name, "Run start, send ",
              self.nb_of_message_2_send,
              "with a pause of 50ms between each one...")
        if(self.message_type == "end"):
            self.broker.publish(self.chanel_name, "End")
            return
        prev_score1 = 70000
        prev_score2 = 100000
        #jobposting = ''
        print(type(prev_score1))
        for counter in range(self.nb_of_message_2_send):
            message, prev_score1, prev_score2 = self.getData(prev_score1,prev_score2,counter)
            print("message is this", message)
            self.broker.publish(self.chanel_name, message)
            time.sleep(0.05)

        print(self.full_thread_name, self.nb_of_message_2_send,
              "sent End to stop chanels listeners.")
    
    def getData(self, prev_score1, prev_score2, counter):
        data = '{"id":"' + str(self.game_id) + '",'
        if(self.chanel_name == "USA"):
            object = jooble_api.job()
            x = object.jobposting
            y = jooble_api.job.jobposting()
            print(type(y))
            job_title = random.choice (y[0])
            job_location = random.choice (y[1])
            job_description = random.choice (y[2])
            #print("job title",job_title)
            #for i in range(0,self.nb_of_message_2_send):
            #data += '"team1":"'+job_title+'","team2":"'+job_location+'",'
            data += '"team1":"'+job_title+'","team2":"'+job_location+'","team3":"'+job_description+'",'
            #data += '"team1":"red", "team2":"blue",'
            prev_score1 = (random.randrange(prev_score1, 100000))
            print(prev_score1)
            prev_score2 = (random.randrange(prev_score2, 120000))
            data += '"score1":"' + str(prev_score1) + '","score2":"' + str(prev_score2)
            data +='"}'
            return data,prev_score1,prev_score2
        elif(self.chanel_name == "India"):
            data += '"team1":"red", "team2":"blue",'
            if(counter % 4 == 0):
                prev_score1 = (random.randrange(prev_score1, prev_score1,1))
                prev_score2 = (random.randrange(prev_score2, prev_score2,1))
            data += '"score1":"' + str(prev_score1) + '","score2":"' + str(prev_score2)
            data +='"}'
            return data,prev_score1,prev_score2

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        thread_name = form.getvalue("sender")
        chanel_name = form.getvalue("channel_name")
        number_of_message_on_channel_1 = int(form.getvalue("num_msg"))
        message_type = (form.getvalue("msg_type"))
        game_id = int(form.getvalue("id"))
        self.send_response(200)
        self.end_headers()
        full_thread_name = "Sender : " + thread_name + " on " + chanel_name
        worker = Sender(thread_name, chanel_name, full_thread_name, number_of_message_on_channel_1, message_type, game_id)
        worker.start()

with HTTPServer(('', 5500), handler) as server:

    server.serve_forever()
