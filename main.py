# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request, jsonify
from google.cloud import pubsub
import base64
import json
from six.moves import http_client

app = Flask(__name__)

# for health check
@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    print "Return a friendly HTTP greeting."
    return 'Welcome to Simple pubsub webservice using Google PubSub API!', 200

"""
  create subscription on a topic
"""
@app.route('/pubsub/topic/<topic_name>/createSub/<subscription_name>', methods=['POST'])
def create_subscription(topic_name, subscription_name):
    """Create a new pull subscription on the given topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    subscription = topic.subscription(subscription_name)
    subscription.create()
    print('Subscription {} created on topic {}.'.format(
        subscription.name, topic.name))
    return 'OK', 200

"""
  delete subscription on topic
"""
@app.route('/pubsub/topic/<topic_name>/deleteSub/<subscription_name>', methods=['POST'])
def delete_subscription(topic_name, subscription_name):
    """Deletes an existing Pub/Sub topic subscriber."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)
    subscription = topic.subscription(subscription_name)
    subscription.delete()
    print('Subscription {} deleted on topic {}.'.format(
        subscription.name, topic.name))
    return 'OK', 200

"""
  Create a topic
"""
@app.route('/pubsub/topic/create/<topic_name>', methods=['POST'])
def create_topic(topic_name):
    """Create a new Pub/Sub topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    topic.create()

    print('Topic {} created.'.format(topic.name))
    return 'OK', 200


"""
  Delete a topic
"""
@app.route('/pubsub/topic/delete/<topic_name>', methods=['POST'])
def delete_topic(topic_name):
    """Deletes an existing Pub/Sub topic."""
    pubsub_client = pubsub.Client()
    topic = pubsub_client.topic(topic_name)

    topic.delete()

    print('Topic {} deleted.'.format(topic.name))
    return 'OK', 200

"""
  Publish messages to a topic
"""
@app.route('/pubsub/topic/<topic_name>/publish', methods=['POST'])
def pushmessage(topic_name):

    # initialze a pubsub client
    ps = pubsub.Client()
    
    # get the topic
    # topic(self, name, timestamp_messages=False)
    topic = ps.topic(topic_name,True)

    # message data
    data = request.json

    # data must be a bytestring
    message=json.dumps(data).encode('utf-8')
    # publish message
    message_id = topic.publish(base64.b64encode(message))
    print('Message {} published.'.format(message_id))

    return 'OK', 200


@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.exception('An error occured while processing the request.')
    response = jsonify({
        'code': http_client.INTERNAL_SERVER_ERROR,
        'message': 'Exception: {}'.format(e)})
    response.status_code = http_client.INTERNAL_SERVER_ERROR
    return response

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    #app.run(host='0.0.0.0', port=8080, debug=True, processes=4, threaded=True)
    app.run(threaded=True,debug=True)
    #app.run(host='127.0.0.1', port=8080, debug=True)
## [END app]


