import sys
import os 
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout, QMessageBox
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
from main_ui import Ui_MainWindow
import json

# Import the engines
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from ii_questionnaire_engine import *
from iii_diagnosis_engine import *
from iv_airway_assessment import *
from v_symptom_assessment import *
from vi_treatment_protocol import *
from vii_long_term_oxygen import *
from viii_lung_intervention_surgery import *
from ix_acute_exacerbation_copd_diagnosis_and_treatment import *
from x_bipap_indication_copd import *
from xi_empirical_antibiotic_selection_outpatient import *
from xii_empirical_antibiotic_selection_inpatient import *

# Define a custom MainWindow class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the UI from the generated 'main_ui' class
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Set window properties
        self.setWindowIcon(QIcon("icon\Logo.png"))
        self.setWindowTitle("Hệ chuyên gia Chuẩn đoán bệnh phổi tắc nghẽn mạn tính")

        # Initialize UI elements
        self.title_label = self.ui.title_label
        self.title_label.setText("CS217.P11 - COPD")

        self.title_icon = self.ui.title_icon
        self.title_icon.setText("")
        self.title_icon.setPixmap(QPixmap(r"interface\icon\Logo.png"))
        self.title_icon.setScaledContents(True)

        self.side_menu = self.ui.listWidget
        self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.main_content = self.ui.stackedWidget
        self.ui.stackedWidget.setCurrentIndex(0)

        # Define a list of menu items with names and icons
        self.menu_list = [
            {
                "name": "1. Thông tin người khám",
            },
            {
                "name": "2. Sàng lọc phát hiện sớm",
            },
            {
                "name": "3. Đo chức năng hô hấp",
            },
            {
                "name": "4. Độ tắc nghẽn đường thở",
            },
            {
                "name": "5. Chuyển đổi điều trị thuốc",
            },
            {
                "name": "6. Chỉ định thở oxi và nội soi",
            },
            {
                "name": "7. Chẩn đoán đợt cấp",
            },
            {
                "name": "8. Thở máy không xâm nhập",
            },
            {
                "name": "9. Thuốc đợt cấp ngoại trú",
            },
            {
                "name": "10. Thuốc đợt cấp nội trú",
            }
        ]

        # Initialize the UI elements and slots
        self.init_list_widget()
        self.init_stackwidget()
        self.init_single_slot()

        # Connect the button click event to the engines
        self.ui.ii_chan_doan_btn.clicked.connect(self.run_i_questionnaire_engine)
        self.ui.iii_chan_doan_1_btn.clicked.connect(self.run_ii_diagnosis_engine)
        self.ui.iii_chan_doan_2_btn.clicked.connect(self.run_iii_airway_assessment)
        self.ui.v_chan_doan_btn.clicked.connect(self.run_v_symptom_assessment)
        self.ui.vi_kiem_tra_btn.clicked.connect(self.run_vi_treatment_protocol)
        self.ui.vii_ket_qua_btn.clicked.connect(self.run_vii_long_term_oxygen)
        self.ui.viii_ket_qua_btn.clicked.connect(self.run_viii_lung_intervention_surgery)



    def init_list_widget(self):
        for item in self.menu_list:
            list_item = QListWidgetItem(item["name"])
            self.side_menu.addItem(list_item)

    def change_tab(self, index):
        self.main_content.setCurrentIndex(index)

    def init_single_slot(self):
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)

    def init_stackwidget(self):
        # Initialize the stack widget with content pages
        widget_list = self.main_content.findChildren(QWidget)

    def load_json(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data
    
    def run_i_questionnaire_engine(self):
        ho = self.ui.ii_ho.isChecked()
        khac_dom = self.ui.ii_khac_dom.isChecked()
        kho_tho = self.ui.ii_kho_tho.isChecked()
        tuoi_tren_40 = self.ui.ii_tuoi_tren_40.isChecked()
        hut_thuoc = self.ui.ii_hut_thuoc.isChecked()

        engine = COPDExpertSystem()
        engine.reset()
        engine.declare(PatientData(ho=ho, khac_dom=khac_dom, kho_tho=kho_tho, tuoi_tren_40=tuoi_tren_40, hut_thuoc=hut_thuoc))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Fact) and fact.get("screening") == "positive":
                self.ui.ii_chan_doan.setText("Kết quả: Có nguy cơ bệnh phổi tắc nghẽn mạn tính. Khuyến cáo đo chức năng hô hấp.")
                return
        self.ui.ii_chan_doan.setText("Kết quả: Không có nguy cơ bệnh phổi tắc nghẽn mạn tính.")

    def run_ii_diagnosis_engine(self):
        fev1_fvc = self.ui.iii_fev1_fvc.value()

        engine = DiagnosisEngine()
        engine.reset()
        engine.declare(LungFunctionData(fev1_fvc=fev1_fvc))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, Fact) and fact.get("copd") is not None:
                if not fact.get("copd"):
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC bình thường. Không mắc BPTNMT.")
                else:
                    self.ui.iii_ket_qua_1.setText("Kết quả: Chỉ số FEV₁/FVC dưới 70%. Chẩn đoán: BPTNMT.")

    def run_iii_airway_assessment(self):
        engine = GOLDStageAssessment()
        engine.reset()

        fev1 = self.ui.iii_fev1.value()

        engine.declare(LungFunctionData(fev1=fev1))
        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, LungFunctionData) and fact.get("GOLD_stage") is not None:
                self.ui.iii_ket_qua_2.setText(f"Kết quả: Giai đoạn {fact.get('GOLD_stage')} - {fact.get('GOLD_stage_description')}")

    def run_v_symptom_assessment(self):
        engine = SymptomAssessment()
        treatment_engine = TreatmentPlan()
        
        engine.reset()
        treatment_engine.reset()

        mMRC = self.ui.v_mmrc.value()
        CAT = sum([self.ui.v_q1.value(), self.ui.v_q2.value(), self.ui.v_q3.value(), self.ui.v_q4.value(), self.ui.v_q5.value(), self.ui.v_q6.value(), self.ui.v_q7.value(), self.ui.v_q8.value()])
        exacerbations = self.ui.v_exacerbations.value()
        hospitalizations = self.ui.v_hospitalizations.value()

        engine.declare(SymptomAssessmentData(mMRC=mMRC, CAT=CAT, exacerbations=exacerbations, hospitalizations=hospitalizations))

        engine.run()

        for fact in engine.facts.values():
            if isinstance(fact, SymptomAssessmentData):
                group = fact.get("group")

        treatment_recommendations = load_json(r"luu_tru_tri_thuc\treatment_recommendations.json")
        general_treatment = []
        recommendations = treatment_recommendations["general_treatment"]
        for recommendation in recommendations:
            general_treatment.append(recommendation)

        treatment_engine.declare(SymptomAssessmentData(group=group, general_treatment=general_treatment))

        treatment_engine.run()
        facts_list = list(treatment_engine.facts.values())
        general_treatment_list = "\n".join([f"- {item}" for item in facts_list[1].get('general_treatment')])
        specific_treatment_list = "\n".join([f"- {item}" for item in facts_list[2].get('specific_treatment')])

        result_text = (
            f"Kết quả: {group}.\n\n"
            f"Phương pháp điều trị chung:\n {general_treatment_list}.\n\n"
            f"Phương pháp điều trị riêng cho {group}:\n {specific_treatment_list}"
        )
        self.ui.v_ket_qua.setText(result_text)
        # msg = QMessageBox()
        # msg.setInformativeText(result_text)
        # msg.setWindowTitle("Kết quả đánh giá triệu chứng")
        # msg.exec()
    
    def run_vi_treatment_protocol(self):
        engine = TreatmentProtocol()
        engine.reset()

        initial_response_text = self.ui.vi_initial_response.currentText()
        initial_response = "positive" if initial_response_text == "Đáp ứng tốt" else "negative"
        status_text = self.ui.vi_status.currentText()
        status = "persistent" if status_text == "Khó thở kéo dài" else "exacerbations"
        current_treatment = self.ui.vi_current_treatment.currentText()
        second_bronchodilator_effective = self.ui.vi_second_bronchodilator_effective.isChecked()
        eosinophils = self.ui.vi_eosinophils.value()
        fev1 = self.ui.vi_fev1.value()
        chronic_bronchitis = self.ui.vi_chronic_bronchitis.isChecked()
        smoker = self.ui.vi_smoker.isChecked()
        severe_side_effects = self.ui.vi_severe_side_effects.isChecked()

        engine.declare(TreatmentData(initial_response=initial_response, status=status, current_treatment=current_treatment, second_bronchodilator_effective=second_bronchodilator_effective, eosinophils=eosinophils, fev1=fev1, chronic_bronchitis=chronic_bronchitis, smoker=smoker, severe_side_effects=severe_side_effects))

        engine.run()

        try:
            result = engine.facts[2].get("treatment_protocol_result")
            self.ui.vi_ket_qua.setText(f"Kết quả: {result}")
        except KeyError:
            self.ui.vi_ket_qua.setText("Không tìm được kết quả.")
    
    def run_vii_long_term_oxygen(self):
        engine = OxygenTherapyEngine()
        engine.reset()

        PaO2 = self.ui.vii_pa02.value()
        SaO2 = self.ui.vii_sa02.value()
        heart_failure = self.ui.vii_heart_failure.isChecked()
        polycythemia = self.ui.vii_polycythemia.isChecked()
        pulmonary_hypertension = self.ui.vii_pulmonary_hypertension.isChecked()

        engine.declare(OxygenAssessment(PaO2=PaO2, SaO2=SaO2, heart_failure=heart_failure, polycythemia=polycythemia, pulmonary_hypertension=pulmonary_hypertension))

        engine.run()

        try:
            oxygen_required = "Chỉ định thở oxy dài hạn.\n" if engine.facts[2].get("oxygen_required") else "Không chỉ định thở oxy.\n"
            long_term_oxygen_reason = "\n".join(engine.facts[2].get("long_term_oxygen_reason"))
            self.ui.vii_ket_qua.setText(f"Kết quả: {oxygen_required}\nLý do:\n{long_term_oxygen_reason}")
        except KeyError:
            self.ui.vii_ket_qua.setText("Không tìm được kết quả.")

    def run_viii_lung_intervention_surgery(self):
        engine = InterventionRecommendation()
        engine.reset()

        emphysema_severity = "nặng" if self.ui.viii_emphysema_severity.currentText() == "Nặng" else "nhẹ"
        lobe_hyperinflation = self.ui.viii_lobe_hyperinflation.isChecked()
        bode_score = self.ui.viii_bode_score.value()
        acute_CO2_exacerbation = self.ui.viii_acute_CO2_exacerbation.isChecked()
        pulmonary_hypertension = self.ui.viii_pulmonary_hypertension.isChecked()
        cor_pulmonale = self.ui.viii_cor_pulmonale.isChecked()
        FEV1 = self.ui.viii_fev1.value()
        DLCO = self.ui.viii_dlco.value()
        emphysema_pattern = "đồng nhất" if self.ui.viii_emphysema_pattern.currentText() == "Đồng nhất" else "không"

        engine.declare(LungInterventionAssessment(emphysema_severity=emphysema_severity, lobe_hyperinflation=lobe_hyperinflation, bode_score=bode_score, acute_CO2_exacerbation=acute_CO2_exacerbation, pulmonary_hypertension=pulmonary_hypertension, cor_pulmonale=cor_pulmonale, FEV1=FEV1, DLCO=DLCO, emphysema_pattern=emphysema_pattern))

        engine.run()

        try:
            diagnosis_result_description = engine.facts[2].get("diagnosis_result_description")
            self.ui.viii_ket_qua.setText(f"Kết quả:\n\n{diagnosis_result_description}")
        except KeyError:
            self.ui.viii_ket_qua.setText("Không tìm được kết quả.")

            

if __name__ == '__main__':
    app = QApplication(sys.argv)

    with open("interface\style.qss") as f:
        style_str = f.read()

    app.setStyleSheet(style_str)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())