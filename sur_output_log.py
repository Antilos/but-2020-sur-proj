class OutputLog:
    def __init__(self):
        self.audio_file = []
        self.image_file = []
        self.audio_target_score = []
        self.audio_non_target_score = []
        self.image_score = []
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

def add_image_scores(score, decisions):
    output_log.image_score = score
    output_log.image_decision = decisions

def work_results():
    # soubor s klasifikaci ciste audia, should be final
    only_audio_file = open("audio_only_classification", "w")
    for name, t_score, a_dec in zip(output_log.audio_file, output_log.audio_target_score, output_log.audio_decision):
        log_line = name + " " + str(t_score) + " " + str(a_dec) + "\n"
        only_audio_file.write(log_line)
    only_audio_file.close()

    # soubor s klasifikaci ciste obrazku, nema score, jen decision, nevim kde to cislo dostat TODO
    only_image_file = open("image_only_classification", "w")
    for name, score, i_dec in zip(output_log.image_file, output_log.image_score, output_log.image_decision):
        log_line = name + " " + str(score) + " " + str(i_dec) + "\n"
        only_image_file.write(log_line)
    only_image_file.close()
    print(len(output_log.image_file), len(output_log.image_score), len(output_log.image_decision))
    pass

