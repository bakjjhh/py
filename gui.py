import tkinter
from tkinter import ttk
import mido
import miditoolkit
import os




window=tkinter.Tk()


window.geometry("640x400+100+100")
window.resizable(False , False )






def button():

    text.delete("1.0" , "end")
    path = os.getcwd()
    midi_path = os.path.join(path, 'midi')
    files = os.listdir(midi_path)

    CHANGE_CONTROL_DICT = {
        1: "Modulation",
        7: "Volume" ,
        11: "Expression",
        64: "Sustain",
    }

    CONTROL_CHANGE_DICT = {v:k for k, v in CHANGE_CONTROL_DICT.items()}

    def get_cc_values(midi_track: mido.MidiTrack, control_change: str):
        """미디 트랙의 control change 값을 리턴하는 함수.
        control_change 는 constants.CONTROL_CHANGE_DICT 의 키 값중 하나를 인자로 받는다.
        """
        if control_change not in CONTROL_CHANGE_DICT.keys():
            raise ValueError
        cc_parameter = CONTROL_CHANGE_DICT[control_change]
        available_cc = set(
            [message.control for message in midi_track if message.type == "control_change"]
        )
        if cc_parameter not in available_cc:
            return None
        cc_values = [
            message.value
            for message in midi_track
            if message.type == "control_change" and message.control == cc_parameter
        ]
        return cc_values

    CHORD_TRACK_NAME = "chord"
    UNKNOWN = "unknown"

    def get_modulation_range(midi_path):
        mido_obj = mido.MidiFile(midi_path)
        for midi_track in mido_obj.tracks[1:]:
            is_chord_track = [message.name for message in midi_track if message.type == "track_name"]
            if CHORD_TRACK_NAME in is_chord_track:
                continue
            modulations = get_cc_values(midi_track, control_change="Modulation")
            if not modulations:
                return UNKNOWN, UNKNOWN
            return min(modulations), max(modulations)
    
    def get_sustain_range(midi_path):
        mido_obj = mido.MidiFile(midi_path)
        for midi_track in mido_obj.tracks[1:]:
            is_chord_track = [message.name for message in midi_track if message.type == "track_name"]
            if CHORD_TRACK_NAME in is_chord_track:
                continue
            sustains = get_cc_values(midi_track, control_change="Sustain")
            if not sustains:
                return UNKNOWN, UNKNOWN
            return min(sustains), max(sustains)

    def get_Expression_range(midi_path):
        mido_obj = mido.MidiFile(midi_path)
        for midi_track in mido_obj.tracks[1:]:
            is_chord_track = [message.name for message in midi_track if message.type == "track_name"]
            if CHORD_TRACK_NAME in is_chord_track:
                continue
            Expressions = get_cc_values(midi_track, control_change="Expression")
            if not Expressions:
                return UNKNOWN, UNKNOWN
            return min(Expressions), max(Expressions)
        
    def get_volume_range(midi_path):
        mido_obj = mido.MidiFile(midi_path)
        for midi_track in mido_obj.tracks[1:]:
            is_chord_track = [message.name for message in midi_track if message.type == "track_name"]
            if CHORD_TRACK_NAME in is_chord_track:
                continue
            volume = get_cc_values(midi_track, control_change="Volume")
            if not volume:
                return UNKNOWN, UNKNOWN
            return min(volume), max(volume)
    
    
    def get_pitch_range(midi_path):
        mido_obj = mido.MidiFile(midi_path)
    
        mididict = []
        output = []
        pitch_list = []


        for midi_track in mido_obj.tracks[1:]:
            track_name = [message.name for message in midi_track if message.type == "track_name"]
            if "chord" in track_name:
                continue
            for i in midi_track:
                if i.type == 'note_on' or i.type == 'note_off':
                    mididict.append(i.dict())


        for midi in mididict:
            
            if midi['type'] == 'note_on' and midi['velocity'] == 1:
                midi['type'] = 'note_off'
            mem2=[]
            if midi['type'] == 'note_on':
                mem2.append(midi['note'])
                output.append(mem2)
        for data in output:
            for pitch_data in data:
                pitch_list.append(pitch_data)

        average_num = int(sum(pitch_list)/len(pitch_list))


        if 24 <= average_num <= 35:
            return "very_low"
        elif 36 <= average_num <= 47:
            return "low"
        elif 48 <= average_num <= 59:
            return "mid_low"
        elif 60 <= average_num <= 71:
            return "mid"
        elif 72 <= average_num <= 83:
            return "mid_high"
        elif 84 <= average_num <= 95:
            return "high"
        else:
            return "very_high"


    
    def get_pitch_wheel_on_off(midi_path):
        mido_obj = mido.MidiFile(midi_path)

        pitch_wheel = ["On" , "Off"]


        for track in mido_obj.tracks[1:]:
            use_tracks = [message.name for message in track if message.type == "track_name"]
            if "chord" in use_tracks:
                continue
            midi_data = [pitch for pitch in track if pitch.type == "pitchwheel"]
        
        
        if len(midi_data) >= 1:
            return pitch_wheel[0]
        else:
            return pitch_wheel[1]
            
        



    def get_velocity_range(
        midi_filename: str, keyswitch_velocity = 1
    ):
        midi_obj = miditoolkit.MidiFile(midi_filename)
        velocities = []
        for track in midi_obj.instruments:
            if track.name == CHORD_TRACK_NAME:
                continue
            for note in track.notes:
                if keyswitch_velocity is not None:
                    if note.velocity != keyswitch_velocity:
                        velocities.append(note.velocity)
                else:
                    velocities.append(note.velocity)

        if not velocities or max(velocities) == 0:
            return UNKNOWN, UNKNOWN
        return min(velocities), max(velocities)


    def get_key_switch_on_off(midi_path):
        mido_obj = mido.MidiFile(midi_path)
    
        mididict = []


        for midi_track in mido_obj.tracks[1:]:
            track_name = [message.name for message in midi_track if message.type == "track_name"]
            if "chord" in track_name:
                continue
            for i in midi_track:
                if i.type == 'note_on':
                    mididict.append(i.dict())

    
        for i in  mididict:
            if i['type'] == 'note_on' and i['velocity'] == 1:
                return "key_switch_on"
        
        return "key_switch_off"



    for file_name in files:
        if file_name.endswith(".mid"):
            tmp_path = os.path.join(midi_path, file_name)
            modulation_result = get_modulation_range(tmp_path), file_name
            sustain_result = get_sustain_range(tmp_path) , file_name
            expression_result = get_Expression_range(tmp_path) , file_name
            volume_result = get_volume_range(tmp_path) , file_name
            pitch_range_result = get_pitch_range(tmp_path) , file_name
            pitch_wheel_result = get_pitch_wheel_on_off(tmp_path) , file_name
            velocity_result = get_velocity_range(tmp_path) , file_name
            key_switch_result = get_key_switch_on_off(tmp_path) , file_name
            modulation_range = str(modulation_result)
            sustain_range = str(sustain_result)
            expression_range = str(expression_result)
            volume_range = str(volume_result)
            pitch_range = str(pitch_range_result)
            pitch_wheel_on_off = str(pitch_wheel_result)
            velocity_range = str(velocity_result)
            key_switch = str(key_switch_result)
            text.insert(tkinter.INSERT  ,"Sustain : " + sustain_range + "\n")
            text.insert(tkinter.INSERT , "Modulation : " + modulation_range + "\n")
            text.insert(tkinter.INSERT , "Expression : " + expression_range + "\n")
            text.insert(tkinter.INSERT , "Volume : " + volume_range + "\n")
            text.insert(tkinter.INSERT , "pitch_range : " + pitch_range + "\n")
            text.insert(tkinter.INSERT , "pitch_wheel : " + pitch_wheel_on_off + "\n")
            text.insert(tkinter.INSERT , "velocity : " + velocity_range + "\n")
            text.insert(tkinter.INSERT , "key_switch : " + key_switch + "\n")
            text.insert(tkinter.INSERT  ,"---------------------------------" + "\n")
















text = tkinter.Text()
text.config(height= 20, width= 70)
text.pack()





btn = tkinter.Button(window
                    ,text = 'average')
btn.config(height = 2 , width = 30 )
btn.config(command = button)
btn.pack(side="bottom")






window.mainloop()