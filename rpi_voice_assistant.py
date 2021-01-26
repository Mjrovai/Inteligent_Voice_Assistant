#!/usr/bin/env python3
# Copyright 2017 Google Inc.
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

"""
Adapted by Marcelo Rovai, @January 2021, based on 2017 original code used as 
demo of the Google Assistant GRPC recognizer.
"""

import time
import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat

from pixels import Pixels
import logging

pixels = Pixels()
pixels.off()

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

def wakeup_assistant():
    pixels.wakeup()
    pixels.think()
    time.sleep(3)
    pixels.speak()
    time.sleep(3)
    pixels.off()

def main():
    wakeup_assistant()
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()
    button = aiy.voicehat.get_button()

    with aiy.audio.get_recorder():
        while True:
            pixels.off()
            status_ui.status('ready')
            print('Press the button and speak')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            pixels.think()
            text, audio = assistant.recognize()
            if text:
                if text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')  
                    pixels.off()
                    time.sleep(1)
                    break
                print('You said "', text, '"')
            if audio:
                pixels.speak()
                aiy.audio.play_audio(audio)
                pixels.off()
    pixels.off()

if __name__ == '__main__':
    main()
