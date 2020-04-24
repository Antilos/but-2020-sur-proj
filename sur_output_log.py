from math import log10
import re

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
    for name, t_score, nt_score, a_dec in zip(output_log.audio_file, output_log.audio_target_score, output_log.audio_non_target_score, output_log.audio_decision):
        name = re.sub(r'^eval[\\\/]','', name)
        log_line = name + " " + str(t_score) + " " + str(a_dec) + "\n"
        only_audio_file.write(log_line)
    only_audio_file.close()

    # soubor s klasifikaci ciste obrazku, nema score, jen decision, nevim kde to cislo dostat TODO
    only_image_file = open("image_only_classification", "w")
    for name, score, i_dec in zip(output_log.image_file, output_log.image_score, output_log.image_decision):
        name = re.sub(r'^eval[\\\/]','', name)
        log_line = name + " " + str(score) + " " + str(i_dec) + "\n"
        only_image_file.write(log_line)
    only_image_file.close()

    # vytvoreni celkovych vysledku
    both_file = open("audio_and_image_classification", "w")
    for file_name, audio_target_score, audio_non_target_score, image_score, audio_decision, image_decision in zip(output_log.audio_file, output_log.audio_target_score, output_log.audio_non_target_score, output_log.image_score, output_log.audio_decision, output_log.image_decision):
        
        if audio_decision: audio_score = audio_target_score
        else: audio_score = audio_non_target_score

        # transform score to a more workable scale
        # audio_score /= 600000

        # if not audio_decision: audio_score = log10(1 - 10**audio_score)

        both_score = (audio_decision + image_score)/2
        if both_score < 0.45: both_decision = 0
        else: both_decision = 1

        file_name = re.sub(r'^eval[\\\/]','', file_name)
        log_line = file_name + " " + str(both_score) + " " + str(both_decision) + "\n"
        both_file.write(log_line)
    both_file.close()
