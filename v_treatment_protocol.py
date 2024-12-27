from experta import *

class TreatmentData(Fact):
    """
    Fact chứa thông tin về điều trị và triệu chứng của bệnh nhân.
    
    Các thuộc tính:
    - initial_response: Phản ứng ban đầu với điều trị (positive/negative)
    - symptoms: Triệu chứng hiện tại (persistent/none)
    - current_treatment: Phác đồ điều trị hiện tại (LABA/LAMA/ICS/LABA/LAMA)
    - second_bronchodilator_effective: Hiệu quả của thuốc giãn phế quản thứ 2
    - exacerbations: Tình trạng đợt cấp (persistent/none)
    - eosinophils: Số lượng bạch cầu ái toan
    - fev1: Chỉ số FEV1 (%)
    - chronic_bronchitis: Tình trạng viêm phế quản mạn tính
    - smoker: Tình trạng hút thuốc
    - severe_side_effects: Tác dụng phụ nghiêm trọng
    """
    initial_response = Field(str)
    symptoms = Field(str)
    current_treatment = Field(str)
    second_bronchodilator_effective = Field(bool)
    exacerbations = Field(str)
    eosinophils = Field(int)
    fev1 = Field(int)
    chronic_bronchitis = Field(bool)
    smoker = Field(bool)
    severe_side_effects = Field(bool)

class TreatmentProtocol(KnowledgeEngine):
    @Rule(TreatmentData(initial_response="positive"))
    def positive_initial_response(self):
        print("Bệnh nhân đáp ứng tốt với phác đồ điều trị ban đầu. Không cần chuyển đổi điều trị thuốc.")

    @Rule(TreatmentData(initial_response="negative", symptoms="persistent", current_treatment="LABA"))
    def laba_persistent_symptoms(self):
        print("Bệnh nhân còn khó thở sau điều trị LABA. Khuyến cáo nâng bậc lên LABA/LAMA.")

    @Rule(TreatmentData(initial_response="negative", symptoms="persistent", current_treatment="LAMA"))
    def lama_persistent_symptoms(self):
        print("Bệnh nhân còn khó thở sau điều trị LAMA. Khuyến cáo nâng bậc lên LABA/LAMA.")

    @Rule(TreatmentData(initial_response="negative", symptoms="persistent", current_treatment="LABA/LAMA", second_bronchodilator_effective=False))
    def laba_lama_no_effect(self):
        print("Thêm thuốc giãn phế quản thứ 2 không cải thiện triệu chứng. Khuyến cáo giảm xuống 1 loại thuốc và xem xét đổi dụng cụ hít hoặc hoạt chất thuốc.")

    @Rule(TreatmentData(initial_response="negative", symptoms="persistent", current_treatment="ICS/LABA"))
    def ics_laba_persistent_symptoms(self):
        print("Bệnh nhân khó thở khi điều trị ICS/LABA. Khuyến cáo nâng bậc lên ICS/LABA/LAMA hoặc chuyển sang LABA/LAMA nếu ICS không phù hợp hoặc có tác dụng phụ.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="LABA"))
    def laba_persistent_exacerbations(self):
        print("Bệnh nhân còn đợt cấp sau điều trị LABA. Khuyến cáo nâng bậc lên LABA/LAMA hoặc ICS/LABA.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="LAMA"))
    def lama_persistent_exacerbations(self):
        print("Bệnh nhân còn đợt cấp sau điều trị LAMA. Khuyến cáo nâng bậc lên LABA/LAMA hoặc ICS/LABA.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="LABA/LAMA", eosinophils=P(lambda e: e >= 100)))
    def laba_lama_exacerbations_high_eosinophils(self):
        print("Bệnh nhân còn đợt cấp với bạch cầu ái toan >= 100 tế bào/µL. Khuyến cáo nâng bậc lên ICS/LABA/LAMA.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="LABA/LAMA", eosinophils=P(lambda e: e < 100)))
    def laba_lama_exacerbations_low_eosinophils(self):
        print("Bệnh nhân còn đợt cấp với bạch cầu ái toan < 100 tế bào/µL. Khuyến cáo thêm Roflumilast hoặc Azithromycin.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA", eosinophils=P(lambda e: e >= 100)))
    def ics_laba_exacerbations_high_eosinophils(self):
        print("Bệnh nhân còn đợt cấp khi điều trị ICS/LABA. Khuyến cáo nâng bậc lên ICS/LABA/LAMA.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA", eosinophils=P(lambda e: e < 100)))
    def ics_laba_exacerbations_low_eosinophils(self):
        print("Bệnh nhân còn đợt cấp khi điều trị ICS/LABA với bạch cầu ái toan < 100 tế bào/µL. Khuyến cáo chuyển sang LABA/LAMA.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA/LAMA", fev1=P(lambda f: f < 50), chronic_bronchitis=True))
    def triple_therapy_exacerbations_with_fev1(self):
        print("Bệnh nhân còn đợt cấp khi điều trị ICS/LABA/LAMA. Khuyến cáo thêm Roflumilast cho bệnh nhân có FEV1 < 50% và viêm phế quản mạn tính.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA/LAMA", smoker=True))
    def triple_therapy_exacerbations_with_smoking(self):
        print("Bệnh nhân còn đợt cấp khi điều trị ICS/LABA/LAMA. Khuyến cáo thêm Azithromycin cho bệnh nhân từng hút thuốc.")

    @Rule(TreatmentData(initial_response="negative", exacerbations="persistent", current_treatment="ICS/LABA/LAMA", severe_side_effects=True))
    def stop_ics_with_side_effects(self):
        print("Bệnh nhân có tác dụng phụ nghiêm trọng khi điều trị ICS/LABA/LAMA. Khuyến cáo ngừng ICS.")

def input_treatment_data():
    initial_response = input("Phản ứng ban đầu với điều trị (positive/negative): ")
    if initial_response.lower() == "positive":
        return TreatmentData(initial_response=initial_response)
    
    symptoms = input("Triệu chứng hiện tại (persistent/none): ")
    current_treatment = input("Phác đồ điều trị hiện tại (LABA/LAMA/ICS/LABA/LAMA): ")
    second_bronchodilator_effective = input("Hiệu quả của thuốc giãn phế quản thứ 2 (True/False): ").lower() == 'true'

    return TreatmentData(
        initial_response=initial_response,
        symptoms=symptoms,
        current_treatment=current_treatment,
        second_bronchodilator_effective=second_bronchodilator_effective
    )

if __name__ == "__main__":
    treatment_engine = TreatmentProtocol()
    treatment_engine.reset()
    treatment_data = input_treatment_data()
    treatment_engine.declare(treatment_data)
    treatment_engine.run()