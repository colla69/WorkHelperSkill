import os
from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler, intent_file_handler
from mycroft.util.log import LOG
import pynput
from alsaaudio import Mixer, mixers as alsa_mixers
from mycroft.skills.audioservice import AudioService


keyboard = pynput.keyboard.Controller()


__author__ = 'colla69'


browserCMD = "sensible-browser"
allCMD = "sensible-browser & skypeforlinux & whatsie &"
pyCharmCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/pycharm-professional_pycharm" \
             "-professional.desktop /snap/bin/pycharm-professional  & "
ideaCMD = "env BAMF_DESKTOP_FILE_HINT=/var/lib/snapd/desktop/applications/intellij-idea-ultimate_intellij-idea" \
          "-ultimate.desktop /snap/bin/intellij-idea-ultimate  & "
raiunoCMD = "firefox 'http://webtvhd.com/rai-uno-live.php' "
xf86_play = 269025044
xf86_stop = 269025045
xf86_prev = 269025046
xf86_next = 269025047


def beamer_screen():
    os.system("xrandr --output DVI-I-2 --mode 1920x1080 --output  DVI-I-3 --off --output HDMI-0 --mode 1920x1080")


def table_screen():
    os.system("xrandr --output DVI-I-2 --mode 1920x1080 --output DVI-I-3 --mode 1920x1080  --right-of DVI-I-2 "
              "--output HDMI-0 --off")


def turn_off_screens():
    os.system("systemctl suspend")


class WorkHelperSkill(MycroftSkill):
    def __init__(self):
        super(WorkHelperSkill, self).__init__(name="TemplateSkill")


    def initialize(self):
        self.add_event('recognizer_loop:record_begin', self.handle_listener_started)
        self.add_event('recognizer_loop:record_end', self.handle_listener_stopped)

    ######################################################################
    # audio ducking
    def handle_listener_started(self, message):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol//3)*2
        Mixer('Master').setvolume(vol)

    def handle_listener_stopped(self, message):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 2) * 3
        if vol > 100:
            vol = 100
        Mixer('Master').setvolume(vol)

    def handle_audio_start(self, event):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 3) * 2
        Mixer('Master').setvolume(vol)

    def handle_audio_stop(self, event):
        vol = Mixer('Master').getvolume()[0]
        vol = (vol // 2) * 3
        if vol > 100:
            vol = 100
        Mixer('Master').setvolume(vol)

    ######################################################################
    # intents
    """
        def handle_beamer_intent(self, message):
            beamer_screen()
            self.speak_dialog("changes.done")
    
        def handle_table_intent(self, message):
            table_screen()
            self.speak_dialog("changes.done")
    """

    @intent_handler(IntentBuilder("TurnOffScreens").require("turn.off.screens"))
    def handle_night_intent(self, message):
        turn_off_screens()

    @intent_handler(IntentBuilder("Dock").require("turn.off.screens"))
    def handle_dock_intent(self, message):
        os.system("xrandr --output DP3-2 --crtc 2 --mode 1920x1200 --pos 0x0 --panning 1920x1200+0+0 --output DP3-1 --crtc 1  --mode 1920x1200 --pos 1920x0 --panning 1920x1200+1920+0 --output eDP1 --crtc 0 --mode 1280x720 --scale 0.5x0.5 --pos 3840x0 --panning 1280x720+3840+0")
    
    @intent_handler(IntentBuilder("UnDock").require("turn.off.screens"))    
    def handle_undock_intent(self, message):
        os.system("xrandr --output DP3-2 --off --output DP3-1 --off --output eDP1 --mode 1920x1080 --scale 1x1")


                  
    @intent_handler(IntentBuilder("BrowserIntent").require("browser"))
    def handle_browser_intent(self, message):
        os.system(browserCMD)

    @intent_handler(IntentBuilder("StackIntent").require("all"))
    def handle_stack_intent(self, message):
        os.system(allCMD)

    @intent_handler(IntentBuilder("PyCharmsIntent").require("open").require("pycharm"))
    def handle_pycharms_intent(self, message):
        os.system(pyCharmCMD)

    @intent_handler(IntentBuilder("IdeaIntent").require("idea"))
    def handle_idea_intent(self, message):
        os.system(ideaCMD)

    @intent_handler(IntentBuilder("PauseMediaIntent").require("pause.media"))
    def handle_pause_media_intent(self, message):
        key = pynput.keyboard.KeyCode.from_vk(xf86_play)
        keyboard.press(key)
        keyboard.release(key)

    @intent_handler(IntentBuilder("RefreshIntent").require("refresh"))
    def handle_refresh_intent(self, message):
        keyboard.press(pynput.keyboard.Key.f5)
        keyboard.release(pynput.keyboard.Key.f5)

    def converse(self, utterances, lang="en-us"):
        # contains all triggerwords for second layer Intents
        return False

    def stop(self):
        pass



def create_skill():
    return WorkHelperSkill()
