import sys
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QMessageBox)
from PyQt5.QtGui import QColor


def plot_emirate_map(emirate):
    shapefile_path = r"C:\Users\user\Downloads\ne_110m_admin_0_countries\ne_110m_admin_0_countries.shp"
    uae_map = gpd.read_file(shapefile_path)

    # Filter for the UAE
    uae_map = uae_map[uae_map['ADMIN'] == "United Arab Emirates"]

    fig, ax = plt.subplots(figsize=(6, 6))
    uae_map.plot(ax=ax, color='gold')

    emirates = {
        'Abu Dhabi': (54.37, 24.47),
        'Dubai': (55.27, 25.20),
        'Sharjah': (55.41, 25.34),
        'Ajman': (55.45, 25.40),
        'Ras Al Khaimah': (55.98, 25.79),
        'Fujairah': (56.34, 25.12),
        'Umm Al Quwain': (55.61, 25.56)
    }

    pisciculture_benefits = {
        'Abu Dhabi': "Abu Dhabi offers ideal coastal conditions and modern infrastructure, making it perfect for large-scale pisciculture.",
        'Dubai': "Dubai's advanced logistics and proximity to international markets provide a solid foundation for commercial fish farming.",
        'Sharjah': "Sharjah's rich maritime heritage and access to the Arabian Gulf make it a promising location for sustainable fish farming.",
        'Ajman': "Ajman has smaller, calm coastal waters, which are beneficial for the controlled breeding of fish species.",
        'Ras Al Khaimah': "Ras Al Khaimah offers a long coastline and natural inlets, making it a strong candidate for both marine and inland pisciculture.",
        'Fujairah': "Fujairah's access to the Gulf of Oman provides unique water conditions that support a variety of fish species.",
        'Umm Al Quwain': "Umm Al Quwain's low population density and clean coastal waters offer a pristine environment for aquaculture."
    }

    # Highlight the selected emirate on the map
    if emirate in emirates:
        x, y = emirates[emirate]
        ax.scatter(x, y, color='black', s=100, label=f'{emirate}')
        ax.text(x + 0.2, y, emirate, fontsize=12, color='black')
        plt.title(f"UAE Map - {emirate} is Highlighted", fontsize=14, color='black')
    else:
        plt.title("UAE Map", fontsize=14, color='yellow')

    ax.set_facecolor('white')  # Change background to white
    ax.tick_params(colors='black')  # Change tick colors to black
    plt.legend(loc='upper left')

    return fig, pisciculture_benefits.get(emirate, "No description available for this emirate.")



# Pisiculture Farming App
class PisicultureApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pisiculture Farm- Quest 1")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: black; color: gold;")  # Change text color to gold

        self.current_screen = "welcome"
        self.current_question = 0
        self.user_conditions = {}

        self.parameters_info = [
            ("pH", "pH is a measure of the acidity or alkalinity of the water. Optimal pH promotes better fish health."),
            ("Temperature (°C)", "Temperature affects fish metabolism and growth. Ideal range is between 25 and 32 °C."),
            ("Turbidity (mg/L)", "Turbidity affects water clarity and fish stress levels. Aim for a turbidity below 50 mg/L."),
            ("Salinity (PSU)", "Salinity is crucial for fish health. Ideal range is 10 to 35 PSU."),
            ("Dissolved Oxygen (mg/L)", "Oxygen is essential for fish respiration. Optimal levels are between 5 and 12 mg/L.")
        ]

        self.ideal_conditions = {
            "pH": 7.5,
            "Temperature (°C)": 28,
            "Turbidity (mg/L)": 30,
            "Salinity PSU": 20,
            "Dissolved Oxygen (mg/L)": 8
        }

        self.emirates = ['Abu Dhabi', 'Dubai', 'Sharjah', 'Ajman', 'Ras Al Khaimah', 'Fujairah', 'Umm Al Quwain']
        self.fish_images = {
            'Tilapia': r'C:\Users\user\Downloads\TILAPIA.jpeg',
            'Catfish': r'C:\Users\user\Downloads\CATFISH.jpeg',
            'Salmon': r'C:\Users\user\Downloads\CARPFISH.jpeg'
        }
        self.selected_emirate = None
        self.selected_fish = None

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.show_welcome_screen()

    def show_welcome_screen(self):
        self.clear_screen()
        title_label = QLabel("Welcome to Your Pisiculture Farm!\nPlease select an Emirate to start your first quest.")
        title_label.setStyleSheet("font-size: 20px; color: gold;")  # Increase title font size
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        for emirate in self.emirates:
            btn = QPushButton(emirate)
            btn.setStyleSheet("background-color: black; color: gold; font-size: 16px; border: 2px solid gold;")  # Change button color to gold
            btn.clicked.connect(lambda _, e=emirate: self.select_emirate(e))
            self.layout.addWidget(btn)

    def select_emirate(self, emirate):
        self.selected_emirate = emirate
        self.show_fish_selection()

    def show_fish_selection(self):
        self.clear_screen()
        title_label = QLabel(f"Selected Emirate: {self.selected_emirate}\nNow, choose a fish type for your farm.")
        title_label.setStyleSheet("font-size: 20px; color: gold;")  # Increase title font size
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)

        for fish, img_path in self.fish_images.items():
            btn = QPushButton(fish)
            btn.setStyleSheet("background-color: black; color: gold; font-size: 16px; border: 2px solid gold;")  # Change button color to gold
            btn.clicked.connect(lambda _, f=fish: self.select_fish(f))
            self.layout.addWidget(btn)

    def select_fish(self, fish):
        self.selected_fish = fish
        self.show_environment_questions()

    def show_environment_questions(self):
        self.clear_screen()
        title_label = QLabel(f"Selected Fish: {self.selected_fish}\nNow, lets evaluate the environmental factors for your emirate.")
        title_label.setStyleSheet("font-size: 20px; color: gold;")  # Increase title font size
        title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title_label)
        self.next_question()

    def next_question(self):
        if self.current_question < len(self.parameters_info):
            param_name, param_info = self.parameters_info[self.current_question]
            question_label = QLabel(param_info)
            question_label.setStyleSheet("font-size: 16px; color: gold;")  # Increase question font size
            question_label.setAlignment(Qt.AlignCenter)
            self.layout.addWidget(question_label)

            self.answer_entry = QLineEdit()
            self.layout.addWidget(self.answer_entry)

            next_button = QPushButton("Next")
            next_button.setStyleSheet("background-color: black; color: gold; border: 2px solid gold;")  # Change button color to gold
            next_button.clicked.connect(self.save_answer_and_next)
            self.layout.addWidget(next_button)
        else:
            self.show_first_graph()

    def save_answer_and_next(self):
        param_name = self.parameters_info[self.current_question][0]
        value = self.answer_entry.text().strip()
        try:
            self.user_conditions[param_name] = float(value)
            self.current_question += 1
            self.clear_screen()
            self.next_question()
        except ValueError:
            QMessageBox.critical(self, "Oh Oh!", f"You must enter a valid number for {param_name}.")

    def show_first_graph(self):
        self.clear_screen()

        fig1, description = plot_emirate_map(self.selected_emirate)

        canvas1 = FigureCanvas(fig1)
        self.layout.addWidget(canvas1)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 16px; color: g;")
        self.layout.addWidget(desc_label)

        # Button to show the next graph
        next_button = QPushButton("Show Environmental Suitability")
        next_button.setStyleSheet("background-color: black; color: gold; border: 2px solid gold;")
        next_button.clicked.connect(self.show_second_graph)
        self.layout.addWidget(next_button)

    def show_second_graph(self):
     self.clear_screen()

     # Calculate suitability score
     suitability_score = self.calculate_suitability_score()

    # Create comparison data
     ideal_values = list(self.ideal_conditions.values())
     user_values = list(self.user_conditions.values())
     parameters = list(self.user_conditions.keys())

     # Plotting the comparison bar chart
     fig2, ax = plt.subplots(figsize=(8, 6))
     x = np.arange(len(parameters))

     # Create a bar chart comparing user values and ideal values
     ax.bar(x - 0.2, ideal_values, 0.4, label='Ideal Values', color='gold')
     ax.bar(x + 0.2, user_values, 0.4, label='Your Values', color='black')

     ax.set_ylabel('Values', color='black',fontsize=10)  # Change label color to black
     ax.set_title('Environmental Parameter Comparison', color='black')  # Change title color to black
     ax.set_xticks(x)
     ax.set_xticklabels(parameters, color='black',fontsize=8)  # Change x-axis tick label color to black
     ax.legend()
     ax.axhline(y=suitability_score, color='red', linestyle='--', label='Suitability Score')

    # Add the score as a label
     ax.text(len(parameters) - 1, suitability_score, f'Suitability Score: {suitability_score:.2f}', 
            color='red', ha='right', va='bottom')

     ax.set_facecolor('white')  # Change background to white
     plt.xticks(color='black')  # Change x-tick color to black
     plt.yticks(color='black')  # Change y-tick color to black

     canvas2 = FigureCanvas(fig2)
     self.layout.addWidget(canvas2)

    # Display suitability score message
     suitability_label = QLabel(f"Calculated Suitability Score: {suitability_score:.2f}/100")
     suitability_label.setStyleSheet("font-size: 18px; color: gold;")
     self.layout.addWidget(suitability_label)

    # Finish button
     finish_button = QPushButton("Finish")
     finish_button.setStyleSheet("background-color: black; color: gold; border: 2px solid gold;")
     finish_button.clicked.connect(self.close_app)
     self.layout.addWidget(finish_button)

     

    def calculate_suitability_score(self):
        score = 0
        for param, ideal_value in self.ideal_conditions.items():
            user_value = self.user_conditions.get(param, ideal_value)
            # Calculate the score as a percentage of how close the user input is to the ideal value
            score += max(0, min(100, (1 - abs(user_value - ideal_value) / ideal_value) * 100))
        return score / len(self.ideal_conditions)

    def clear_screen(self):
        for i in reversed(range(self.layout.count())):
            widget = self.layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def close_app(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PisicultureApp()
    window.show()
    sys.exit(app.exec_())
