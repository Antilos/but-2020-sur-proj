class OutputLog:
    def __init__(self):
        self.audio_file = []
        self.image_file = []
        self.audio_target_score = []
        self.audio_non_target_score = []
        self.audio_decision = []
        self.image_decision = []


output_log = OutputLog()


def add_audio_file(file):
    file_name, end = file.split('.')
    output_log.audio_file.append(file_name)


def add_image_file(file):
    file_name, end = file.split('.')
    output_log.image_file.append(file_name)


def add_audio_scores(target_score, non_target_score, decision):
    output_log.audio_target_score.append(target_score)
    output_log.audio_non_target_score.append(non_target_score)
    output_log.audio_decision.append(decision)

def add_image_scores(decisions):
    output_log.image_decision = decisions

def work_results():
    # print(output_log.audio_file)
    for name, t_score, nt_score, a_dec, i_dec in zip(output_log.audio_file, output_log.audio_target_score, output_log.audio_non_target_score, output_log.audio_decision, output_log.image_decision):
        print(name, t_score, nt_score, a_dec, i_dec)
    pass

