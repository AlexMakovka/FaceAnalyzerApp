import cv2
import os
import csv
from datetime import datetime
import matplotlib.pyplot as plt

def save_frame(frame):
    if not os.path.exists('captures'):
        os.makedirs('captures')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join('captures', f"capture_{timestamp}.png")
    cv2.imwrite(filename, frame)

def log_result(gender, age, emotion):
    file_path = 'results.csv'
    write_header = not os.path.isfile(file_path)
    with open(file_path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(['gender', 'age', 'emotion'])
        writer.writerow([gender, age, emotion])

def create_statistics_figure():
    file_path = 'results.csv'
    if not os.path.isfile(file_path):
        return None
    genders, ages, emotions = [], [], []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            genders.append(row['gender'])
            try:
                ages.append(int(row['age']))
            except:
                continue
            emotions.append(row['emotion'])
    if not genders or not ages or not emotions:
        return None
    fig, axs = plt.subplots(1, 3, figsize=(12, 4))
    gender_counts = {g: genders.count(g) for g in set(genders)}
    axs[0].bar(gender_counts.keys(), gender_counts.values(), color=['#4c72b0', '#c44e52'])
    axs[0].set_title("Распределение по полу")
    axs[1].hist(ages, bins=range(0, 101, 10), color='#55a868', edgecolor='black')
    axs[1].set_title("Распределение по возрасту")
    emotion_counts = {e: emotions.count(e) for e in set(emotions)}
    sorted_emotions = sorted(emotion_counts.items(), key=lambda x: -x[1])
    axs[2].bar([e[0] for e in sorted_emotions], [e[1] for e in sorted_emotions], color='#8172b3')
    axs[2].set_title("Распределение по эмоциям")
    plt.tight_layout()
    return fig