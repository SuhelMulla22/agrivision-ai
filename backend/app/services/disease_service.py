"""
Disease Knowledge Base Service — rich information about crop diseases.

Contains detailed disease info including descriptions, symptoms, causes,
treatment (organic + chemical), and prevention tips — in EN/HI/MR.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class DiseaseService:
    """Provides disease information from the knowledge base."""

    def __init__(self):
        self._knowledge_base: Dict[str, Dict] = {}
        self._load_knowledge_base()

    def _load_knowledge_base(self) -> None:
        """Load disease knowledge from JSON file."""
        kb_path = Path("data/disease_knowledge.json")
        if kb_path.exists():
            with open(kb_path, "r", encoding="utf-8") as f:
                self._knowledge_base = json.load(f)
            logger.info(f"Loaded {len(self._knowledge_base)} diseases from knowledge base.")
        else:
            logger.warning("Disease knowledge base not found. Using built-in defaults.")
            self._load_builtin_knowledge()

    def _load_builtin_knowledge(self) -> None:
        """Built-in disease knowledge — curated for Indian agriculture."""
        self._knowledge_base = {
            "tomato_early_blight": {
                "name": {"en": "Early Blight", "hi": "अर्ली ब्लाइट", "mr": "अर्ली ब्लाइट"},
                "crop": "Tomato",
                "description": {
                    "en": "Early blight is a common fungal disease caused by Alternaria solani. It affects tomato plants at all growth stages, causing dark concentric ring-shaped lesions on leaves.",
                    "hi": "अर्ली ब्लाइट एक सामान्य कवक रोग है जो Alternaria solani के कारण होता है। यह टमाटर के पौधों को सभी विकास चरणों में प्रभावित करता है।",
                    "mr": "अर्ली ब्लाइट हा Alternaria solani या बुरशीमुळे होणारा सामान्य रोग आहे. हे टोमॅटोच्या रोपांना सर्व वाढीच्या टप्प्यांवर प्रभावित करते.",
                },
                "symptoms": {
                    "en": ["Dark concentric rings on leaves (bull's eye pattern)", "Yellowing around lesions", "Premature leaf drop", "Stem lesions near soil line", "Fruit rot on shoulders"],
                    "hi": ["पत्तियों पर गहरे गोलाकार छल्ले (बैल की आंख जैसा पैटर्न)", "घावों के चारों ओर पीलापन", "समय से पहले पत्तियों का गिरना", "तने पर घाव", "फलों के कंधे पर सड़न"],
                    "mr": ["पानांवर काळे गोलाकार रिंग (बैलचे डोळे सारखे)", "जखमांभोवती पिवळसरपणा", "काळापूर्वी पाने गळणे", "देठावर जखम", "फळांच्या शेजारी कुजणे"],
                },
                "causes": {
                    "en": ["Alternaria solani fungal infection", "Warm humid weather (24-29°C)", "Wet foliage from overhead irrigation", "Poor air circulation", "Nutrient-deficient soil"],
                    "hi": ["Alternaria solani कवक संक्रमण", "गर्म आर्द्र मौसम (24-29°C)", "ओवरहेड सिंचाई से गीली पत्तियां", "कम हवा का प्रवाह", "पोषक तत्वों की कमी वाली मिट्टी"],
                    "mr": ["Alternaria solani बुरशीजन्य संसर्ग", "उष्ण दमट हवामान (24-29°C)", "वरून पाणी दिल्याने ओली पाने", "कमी हवेचा प्रवाह", "पोषकद्रव्यं कमी असलेली माती"],
                },
                "treatment": {
                    "organic": {
                        "en": ["Remove and destroy infected plant material", "Apply neem oil spray (5ml/L water)", "Use Trichoderma viride bio-fungicide", "Apply compost tea as foliar spray", "Mulch around plants to prevent soil splash"],
                        "hi": ["संक्रमित पौध सामग्री हटाएं और नष्ट करें", "नीम तेल का छिड़काव करें (5 मिली/लीटर पानी)", "ट्राइकोडर्मा विरिडे जैविक कवकनाशी का उपयोग करें", "कम्पोस्ट चाय का पत्ती पर छिड़काव करें", "पौधों के चारों ओर मल्च बिछाएं"],
                        "mr": ["संक्रमित वनस्पती साहित्य काढून नष्ट करा", "कडुलिंब तेल फवारणी (5 मिली/लिटर पाणी)", "ट्रायकोडर्मा विरिडे जैविक औषध वापरा", "कम्पोस्ट चहा पानांवर फवारा", "रोपांभोवती गाळ द्या"],
                    },
                    "chemical": {
                        "en": ["Mancozeb 75% WP @ 2g/L water (prophylactic)", "Metalaxyl + Mancozeb @ 2.5g/L", "Azoxystrobin 23% SC @ 1ml/L", "Chlorothalonil 75% WP @ 2g/L", "Spray every 7-10 days, rotate fungicides"],
                        "hi": ["मैंकोज़ेब 75% WP @ 2g/L पानी (रोकथाम के लिए)", "मेटालैक्सिल + मैंकोज़ेब @ 2.5g/L", "एज़ोक्सीस्ट्रोबिन 23% SC @ 1ml/L", "हर 7-10 दिन में छिड़काव करें, कवकनाशी बदलें"],
                        "mr": ["मँकोझेब 75% WP @ 2g/L पाणी (प्रतिबंधात्मक)", "मेटालॅक्सिल + मँकोझेब @ 2.5g/L", "अझोक्सिस्ट्रोबिन 23% SC @ 1ml/L", "दर 7-10 दिवसांनी फवारणी करा, औषधे बदलत राहा"],
                    },
                },
                "prevention": {
                    "en": ["Use certified disease-free seeds", "Practice 3-year crop rotation", "Ensure adequate plant spacing (60cm)", "Water at base, avoid wetting foliage", "Apply balanced NPK fertilizer", "Remove plant debris after harvest"],
                    "hi": ["प्रमाणित रोग-मुक्त बीजों का उपयोग करें", "3 साल की फसल चक्र का पालन करें", "पर्याप्त पौध दूरी सुनिश्चित करें (60cm)", "जड़ में पानी दें, पत्तियों को गीला करने से बचें", "संतुलित NPK उर्वरक डालें", "फसल के बाद पौधों का मलबा हटाएं"],
                    "mr": ["प्रमाणित रोगमुक्त बियाणे वापरा", "3 वर्षांची पीक चक्र पद्धती अवलंबा", "पुरेशी रोपांमधील अंतर ठेवा (60cm)", "मुळाशी पाणी द्या, पाने ओली करू नका", "संतुलित NKB खत द्या", "कापणीनंतर वनस्पती अवशेष काढून टाका"],
                },
                "severity_info": {
                    "high": {"en": "Immediate action required. Disease is actively spreading.", "hi": "तत्काल कार्रवाई आवश्यक। रोग सक्रिय रूप से फैल रहा है।", "mr": "त्वरित कार्यवाही आवश्यक. रोग सक्रियपणे पसरत आहे."},
                    "moderate": {"en": "Monitor closely. Apply preventive treatment.", "hi": "बारीकी से निगरानी करें। निवारक उपचार लागू करें।", "mr": "बारकाईने निरीक्षण करा. प्रतिबंधात्मक उपचार करा."},
                    "low": {"en": "Early stage detected. Preventive measures recommended.", "hi": "प्रारंभिक अवस्था का पता चला। निवारक उपायों की सिफारिश की जाती है।", "mr": "सुरुवाती टप्पा आढळला. प्रतिबंधात्मक उपाय शिफारस केले जातात."},
                },
            },
            "tomato_late_blight": {
                "name": {"en": "Late Blight", "hi": "लेट ब्लाइट", "mr": "लेट ब्लाइट"},
                "crop": "Tomato",
                "description": {
                    "en": "Late blight is a devastating disease caused by Phytophthora infestans. It can destroy entire fields within days under favorable conditions (cool, wet weather).",
                    "hi": "लेट ब्लाइट Phytophthora infestans के कारण होने वाला एक विनाशकारी रोग है। अनुकूल परिस्थितियों में यह पूरे खेत को कुछ दिनों में नष्ट कर सकता है।",
                    "mr": "लेट ब्लाइट हा Phytophthora infestans यामुळे होणारा विनाशकारी रोग आहे. अनुकूल परिस्थितीत हे काही दिवसांत संपूर्ण शेत नष्ट करू शकते.",
                },
                "symptoms": {
                    "en": ["Water-soaked dark lesions on leaves", "White fuzzy growth on leaf undersides", "Rapid browning and death of foliage", "Dark brown lesions on stems", "Firm, dark brown rot on green fruits"],
                    "hi": ["पत्तियों पर पानी से भरे गहरे धब्बे", "पत्तियों के नीचे सफेद रोंयेदार वृद्धि", "पत्तियों का तेजी से भूरा होना और मरना", "तनों पर गहरे भूरे धब्बे", "हरे फलों पर कठोर, गहरा भूरा सड़न"],
                    "mr": ["पानांवर पाण्याने भरलेले काळे ठिपके", "पानांच्या खाली पांढरे रेशेदार वाढ", "पानांचा जलद पिवळसर-भडक रंग आणि मृत्यू", "देठावर गडद तपकिरी ठिपके", "हिरव्या फळांवर घट्ट, गडद तपकिरी कुजणे"],
                },
                "causes": {
                    "en": ["Phytophthora infestans (oomycete pathogen)", "Cool temperatures (15-25°C)", "High humidity (>90%)", "Prolonged leaf wetness (6+ hours)", "Infected seed potatoes or transplants"],
                    "hi": ["Phytophthora infestans (ऊष्मप्रबल रोगज़नक़)", "ठंडा तापमान (15-25°C)", "अधिक आर्द्रता (>90%)", "लंबे समय तक पत्तियों का गीलापन (6+ घंटे)", "संक्रमित बीज आलू या रोपाई"],
                    "mr": ["Phytophthora infestans (ऊष्मप्रबल रोगजनक)", "थंड तापमान (15-25°C)", "जास्त आर्द्रता (>90%)", "दीर्घकाळ पाने ओली राहणे (6+ तास)", "संक्रमित बियाणे बटाटा किंवा रोपे"],
                },
                "treatment": {
                    "organic": {
                        "en": ["Immediately remove and destroy infected plants", "Apply copper-based fungicide (Bordeaux mixture)", "Increase plant spacing for air circulation", "Remove lower leaves touching soil", "Apply Trichoderma-based bio-fungicide preventively"],
                        "hi": ["तुरंत संक्रमित पौधों को हटाकर नष्ट करें", "कॉपर आधारित कवकनाशी लगाएं (बोर्डो मिश्रण)", "हवा के प्रवाह के लिए पौध दूरी बढ़ाएं", "मिट्टी को छूने वाली निचली पत्तियां हटाएं", "ट्राइकोडर्मा आधारित जैविक कवकनाशी का निवारक छिड़काव करें"],
                        "mr": ["ताबडतोब संक्रमित रोपे काढून नष्ट करा", "कॉपरयुक्त बुरशीनाशक वापरा (बोर्डो मिश्रण)", "हवेचा प्रवाह वाढवण्यासाठी रोपांमधील अंतर वाढवा", "मातीला स्पर्श करणारी खालची पाने काढा", "ट्रायकोडर्मा आधारित जैविक औषध प्रतिबंधात्मक फवारा"],
                    },
                    "chemical": {
                        "en": ["Metalaxyl-M + Mancozeb @ 2.5g/L (systemic)", "Dimethomorph + Mancozeb @ 2g/L", "Cymoxanil + Mancozeb @ 2.5g/L", "Fenamidone + Mancozeb @ 1.5g/L", "Spray at first sign, repeat every 5-7 days"],
                        "hi": ["मेटालैक्सिल-एम + मैंकोज़ेब @ 2.5g/L (प्रणालीगत)", "डाइमेथोमॉर्फ + मैंकोज़ेब @ 2g/L", "पहले लक्षण पर छिड़काव करें, हर 5-7 दिन में दोहराएं"],
                        "mr": ["मेटालॅक्सिल-एम + मँकोझेब @ 2.5g/L (प्रणालीगत)", "डायमेथोमॉर्फ + मँकोझेब @ 2g/L", "पहिल्या लक्षणावर फवारणी करा, दर 5-7 दिवसांनी दोहरा"],
                    },
                },
                "prevention": {
                    "en": ["Use resistant varieties (e.g., Arka Rakshak, Himsona)", "Avoid overhead irrigation", "Monitor weather forecasts for blight-favorable conditions", "Destroy volunteer potato/tomato plants", "Apply preventive fungicide during wet weather"],
                    "hi": ["प्रतिरोधी किस्मों का उपयोग करें (जैसे अर्का रक्षक, हिमसोना)", "ओवरहेड सिंचाई से बचें", "ब्लाइट-अनुकूल मौसम के पूर्वानुमान की निगरानी करें", "स्वयंभू आलू/टमाटर के पौधों को नष्ट करें", "गीले मौसम में निवारक कवकनाशी लगाएं"],
                    "mr": ["प्रतिरोधक जाती वापरा (उदा. अर्का रक्षक, हिमसोना)", "वरून पाणी देणे टाळा", "ब्लाइट-अनुकूल हवामानाचा अंदाज बघा", "स्वयंभू बटाटा/टोमॅटो रोपे नष्ट करा", "ओल्या हवामानात प्रतिबंधात्मक बुरशीनाशक फवारा"],
                },
                "severity_info": {
                    "high": {"en": "CRITICAL: Act immediately. Late blight spreads extremely fast.", "hi": "गंभीर: तुरंत कार्रवाई करें। लेट ब्लाइट बहुत तेजी से फैलता है।", "mr": "गंभीर: लगेच कृती करा. लेट ब्लाइट अत्यंत वेगाने पसरतो."},
                    "moderate": {"en": "Risk is elevated. Apply protective treatment immediately.", "hi": "जोखिम बढ़ गया है। तुरंत सुरक्षात्मक उपचार लागू करें।", "mr": "धोका वाढला आहे. लगेच संरक्षणात्मक उपचार करा."},
                    "low": {"en": "Conditions favorable for blight. Start preventive spraying.", "hi": "ब्लाइट के लिए अनुकूल स्थितियां। निवारक छिड़काव शुरू करें।", "mr": "ब्लाइटसाठी अनुकूल परिस्थिती. प्रतिबंधात्मक फवारणी सुरू करा."},
                },
            },
            "tomato_healthy": {
                "name": {"en": "Healthy", "hi": "स्वस्थ", "mr": "निरोगी"},
                "crop": "Tomato",
                "description": {
                    "en": "The plant appears healthy with no visible signs of disease. Continue regular care and monitoring.",
                    "hi": "पौधा स्वस्थ प्रतीत होता है। रोग के कोई दृश्य संकेत नहीं हैं। नियमित देखभाल जारी रखें।",
                    "mr": "रोप निरोगी दिसते. रोगाची कोणतीही दृश्य चिन्हे नाहीत. नियमित काळजी चालू ठेवा.",
                },
                "symptoms": {"en": ["No disease symptoms detected"], "hi": ["कोई रोग लक्षण नहीं मिला"], "mr": ["कोणतेही रोग लक्षण आढळले नाही"]},
                "causes": {"en": ["N/A — plant is healthy"], "hi": ["N/A — पौधा स्वस्थ है"], "mr": ["N/A — रोप निरोगी आहे"]},
                "treatment": {
                    "organic": {"en": ["No treatment needed"], "hi": ["कोई उपचार आवश्यक नहीं"], "mr": ["कोणत्याही उपचारांची गरज नाही"]},
                    "chemical": {"en": ["No treatment needed"], "hi": ["कोई उपचार आवश्यक नहीं"], "mr": ["कोणत्याही उपचारांची गरज नाही"]},
                },
                "prevention": {
                    "en": ["Maintain regular watering schedule", "Apply balanced fertilizer monthly", "Monitor weekly for early signs", "Keep area weed-free"],
                    "hi": ["नियमित पानी का कार्यक्रम बनाए रखें", "मासिक संतुलित उर्वरक डालें", "शुरुआती संकेतों के लिए साप्ताहिक निगरानी करें", "क्षेत्र को खरपतवार मुक्त रखें"],
                    "mr": ["नियमित पाणी देण्याचे वेळापत्रक ठेवा", "दरमहाने संतुलित खत द्या", "सुरुवातीच्या चिन्हांसाठी साप्ताहिक तपासणी करा", "क्षेत्र तणमुक्त ठेवा"],
                },
                "severity_info": {
                    "high": None,
                    "moderate": None,
                    "low": None,
                },
            },
        }

        # Add more diseases for other crops (potato, corn, rice, cotton, etc.)
        self._add_crop_diseases()

    def _add_crop_diseases(self) -> None:
        """Add diseases for additional crops."""
        additional = {
            "potato_early_blight": {
                "name": {"en": "Early Blight", "hi": "अर्ली ब्लाइट", "mr": "अर्ली ब्लाइट"},
                "crop": "Potato",
                "description": {
                    "en": "Early blight in potato is caused by Alternaria solani. It produces dark, target-like lesions on lower leaves and can reduce yield by 20-30%.",
                    "hi": "आलू में अर्ली ब्लाइट Alternaria solani के कारण होता है। यह निचली पत्तियों पर गहरे, लक्ष्य जैसे धब्बे बनाता है।",
                    "mr": "बटाट्यातील अर्ली ब्लाइट Alternaria solani यामुळे होतो. खालच्या पानांवर गडद, लक्ष्य सारखे ठिपके बनवतो.",
                },
                "symptoms": {"en": ["Dark concentric lesions on lower leaves", "Yellowing and wilting of affected leaves", "Tuber lesions with dark, sunken areas"], "hi": ["निचली पत्तियों पर गहरे गोलाकार धब्बे", "प्रभावित पत्तियों का पीलापन और मुरझाना"], "mr": ["खालच्या पानांवर गडद गोलाकार ठिपके", "प्रभावित पानांचा पिवळसरपणा आणि मुरझणे"]},
                "causes": {"en": ["Alternaria solani", "Warm temperatures (24-29°C)", "High humidity"], "hi": ["Alternaria solani", "गर्म तापमान (24-29°C)", "अधिक आर्द्रता"], "mr": ["Alternaria solani", "उष्ण तापमान (24-29°C)", "जास्त आर्द्रता"]},
                "treatment": {"organic": {"en": ["Crop rotation (3+ years)", "Remove infected debris", "Apply neem oil spray"], "hi": ["फसल चक्र (3+ वर्ष)", "संक्रमित मलबा हटाएं"], "mr": ["पीक चक्र (3+ वर्षे)", "संक्रमित अवशेष काढा"]}, "chemical": {"en": ["Mancozeb 75% WP @ 2g/L", "Chlorothalonil 75% WP @ 2g/L"], "hi": ["मैंकोज़ेब 75% WP @ 2g/L"], "mr": ["मँकोझेब 75% WP @ 2g/L"]}},
                "prevention": {"en": ["Use certified seed potatoes", "Ensure good drainage", "Maintain plant spacing"], "hi": ["प्रमाणित बीज आलू का उपयोग करें", "अच्छी जल निकासी सुनिश्चित करें"], "mr": ["प्रमाणित बियाणे बटाटा वापरा", "चांगला निचरा सुनिश्चित करा"]},
                "severity_info": {"high": {"en": "Immediate treatment needed.", "hi": "तत्काल उपचार आवश्यक।", "mr": "त्वरित उपचार आवश्यक."}, "moderate": {"en": "Apply preventive treatment.", "hi": "निवारक उपचार लागू करें।", "mr": "प्रतिबंधात्मक उपचार करा."}, "low": {"en": "Monitor closely.", "hi": "बारीकी से निगरानी करें।", "mr": "बारकाईने निरीक्षण करा."}},
            },
            "potato_late_blight": {
                "name": {"en": "Late Blight", "hi": "लेट ब्लाइट", "mr": "लेट ब्लाइट"},
                "crop": "Potato",
                "description": {"en": "Late blight, caused by Phytophthora infestans, is the disease that caused the Irish Potato Famine. It can destroy entire potato fields within days.", "hi": "लेट ब्लाइट Phytophthora infestans के कारण होता है। यह कुछ दिनों में पूरे आलू के खेत को नष्ट कर सकता है।", "mr": "लेट ब्लाइट Phytophthora infestans यामुळे होतो. हे काही दिवसांत संपूर्ण बटाट्याचे शेत नष्ट करू शकते."},
                "symptoms": {"en": ["Water-soaked lesions on leaves", "White sporulation on leaf undersides", "Rapid plant death", "Reddish-brown dry rot in tubers"], "hi": ["पत्तियों पर पानी जैसे धब्बे", "पत्तियों के नीचे सफेद बीजाणु"], "mr": ["पानांवर पाण्यासारखे ठिपके", "पानांच्या खाली पांढरे बीजाणू"]},
                "causes": {"en": ["Phytophthora infestans", "Cool wet weather (15-25°C)", "High humidity"], "hi": ["Phytophthora infestans", "ठंडा गीला मौसम"], "mr": ["Phytophthora infestans", "थंड ओले हवामान"]},
                "treatment": {"organic": {"en": ["Destroy infected plants immediately", "Apply copper fungicide"], "hi": ["संक्रमित पौधों को तुरंत नष्ट करें"], "mr": ["संक्रमित रोपे लगेच नष्ट करा"]}, "chemical": {"en": ["Metalaxyl + Mancozeb @ 2.5g/L", "Cymoxanil + Mancozeb"], "hi": ["मेटालैक्सिल + मैंकोज़ेब @ 2.5g/L"], "mr": ["मेटालॅक्सिल + मँकोझेब @ 2.5g/L"]}},
                "prevention": {"en": ["Use resistant varieties", "Avoid overhead irrigation", "Monitor weather"], "hi": ["प्रतिरोधी किस्मों का उपयोग करें"], "mr": ["प्रतिरोधक जाती वापरा"]},
                "severity_info": {"high": {"en": "CRITICAL: Act immediately.", "hi": "गंभीर: तुरंत कार्रवाई करें।", "mr": "गंभीर: लगेच कृती करा."}, "moderate": {"en": "Apply treatment urgently.", "hi": "तुरंत उपचार करें।", "mr": "त्वरित उपचार करा."}, "low": {"en": "Start preventive measures.", "hi": "निवारक उपाय शुरू करें।", "mr": "प्रतिबंधात्मक उपाय सुरू करा."}},
            },
            "potato_healthy": {
                "name": {"en": "Healthy", "hi": "स्वस्थ", "mr": "निरोगी"},
                "crop": "Potato",
                "description": {"en": "Plant appears healthy.", "hi": "पौधा स्वस्थ दिखता है।", "mr": "रोप निरोगी दिसते."},
                "symptoms": {"en": ["No symptoms"], "hi": ["कोई लक्षण नहीं"], "mr": ["कोणतेही लक्षण नाही"]},
                "causes": {"en": ["N/A"], "hi": ["N/A"], "mr": ["N/A"]},
                "treatment": {"organic": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}, "chemical": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}},
                "prevention": {"en": ["Continue regular care"], "hi": ["नियमित देखभाल जारी रखें"], "mr": ["नियमित काळजी चालू ठेवा"]},
                "severity_info": {"high": None, "moderate": None, "low": None},
            },
            "corn_common_rust": {
                "name": {"en": "Common Rust", "hi": "कॉमन रस्ट", "mr": "कॉमन रस्ट"},
                "crop": "Corn",
                "description": {"en": "Common rust of corn is caused by Puccinia sorghi. It produces cinnamon-brown pustules on leaves.", "hi": "मक्का का कॉमन रस्ट Puccinia sorghi के कारण होता है।", "mr": "मक्क्यातील कॉमन रस्ट Puccinia sorghi यामुळे होतो."},
                "symptoms": {"en": ["Cinnamon-brown oval pustules on leaves", "Pustules on both leaf surfaces", "Severe infection causes leaf death"], "hi": ["पत्तियों पर दालचीनी-भूरे अंडाकार धब्बे"], "mr": ["पानांवर दालचिनी-तपकिरी अंडाकार फोड"]},
                "causes": {"en": ["Puccinia sorghi fungus", "Cool humid weather"], "hi": ["Puccinia sorghi कवक"], "mr": ["Puccinia sorghi बुरशी"]},
                "treatment": {"organic": {"en": ["Remove infected leaves", "Apply sulfur-based fungicide"], "hi": ["संक्रमित पत्तियां हटाएं"], "mr": ["संक्रमित पाने काढा"]}, "chemical": {"en": ["Propiconazole 25% EC @ 1ml/L", "Tebuconazole 25.9% EC @ 1ml/L"], "hi": ["प्रोपिकोनाज़ोल 25% EC @ 1ml/L"], "mr": ["प्रोपिकोनाझोल 25% EC @ 1ml/L"]}},
                "prevention": {"en": ["Plant resistant hybrids", "Practice crop rotation"], "hi": ["प्रतिरोधी संकर लगाएं"], "mr": ["प्रतिरोधक संकर लावा"]},
                "severity_info": {"high": {"en": "Apply fungicide immediately.", "hi": "तुरंत कवकनाशी लगाएं।", "mr": "लगेच बुरशीनाशक फवारा."}, "moderate": {"en": "Monitor and prepare treatment.", "hi": "निगरानी करें और उपचार तैयार करें।", "mr": "निरीक्षण करा आणि उपचार तयार करा."}, "low": {"en": "Early stage, preventive measures sufficient.", "hi": "प्रारंभिक अवस्था, निवारक उपाय पर्याप्त।", "mr": "सुरुवाती टप्पा, प्रतिबंधात्मक उपाय पुरेसे."}},
            },
            "corn_healthy": {
                "name": {"en": "Healthy", "hi": "स्वस्थ", "mr": "निरोगी"},
                "crop": "Corn",
                "description": {"en": "Plant appears healthy.", "hi": "पौधा स्वस्थ दिखता है।", "mr": "रोप निरोगी दिसते."},
                "symptoms": {"en": ["No symptoms"], "hi": ["कोई लक्षण नहीं"], "mr": ["कोणतेही लक्षण नाही"]},
                "causes": {"en": ["N/A"], "hi": ["N/A"], "mr": ["N/A"]},
                "treatment": {"organic": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}, "chemical": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}},
                "prevention": {"en": ["Continue regular care"], "hi": ["नियमित देखभाल जारी रखें"], "mr": ["नियमित काळजी चालू ठेवा"]},
                "severity_info": {"high": None, "moderate": None, "low": None},
            },
            "rice_bacterial_leaf_blight": {
                "name": {"en": "Bacterial Leaf Blight", "hi": "बैक्टीरियल लीफ ब्लाइट", "mr": "बॅक्टेरियल लीफ ब्लाइट"},
                "crop": "Rice",
                "description": {"en": "Bacterial leaf blight (BLB) is caused by Xanthomonas oryzae. It is one of the most serious diseases of rice in India, causing yield losses of 20-50%.", "hi": "बैक्टीरियल लीफ ब्लाइट Xanthomonas oryzae के कारण होता है। यह भारत में धान का सबसे गंभीर रोग है।", "mr": "बॅक्टेरियल लीफ ब्लाइट Xanthomonas oryzae यामुळे होतो. हा भारतातील भाताचा सर्वात गंभीर रोग आहे."},
                "symptoms": {"en": ["Water-soaked lesions on leaf tips", "Yellow-orange stripes along leaf veins", "Bacterial ooze on leaf surface (milky droplets)", "Complete leaf drying"], "hi": ["पत्तियों की नोक पर पानी जैसे धब्बे", "पत्ती शिराओं के साथ पीले-नारंगी धारियां"], "mr": ["पानांच्या टोकावर पाण्यासारखे ठिपके", "पान शिरांसोबत पिवळे-नारिंगी पट्टे"]},
                "causes": {"en": ["Xanthomonas oryzae pv. oryzae", "High humidity and temperature (25-30°C)", "Wound entry through leaf tips", "Contaminated irrigation water"], "hi": ["Xanthomonas oryzae pv. oryzae", "अधिक आर्द्रता और तापमान"], "mr": ["Xanthomonas oryzae pv. oryzae", "जास्त आर्द्रता आणि तापमान"]},
                "treatment": {"organic": {"en": ["Remove infected plants", "Apply Pseudomonas fluorescens @ 10g/L", "Use Trichoderma viride"], "hi": ["संक्रमित पौधे हटाएं"], "mr": ["संक्रमित रोपे काढा"]}, "chemical": {"en": ["Streptocycline 500ppm + Copper oxychloride @ 3g/L", "Bordeaux mixture 1%"], "hi": ["स्ट्रेप्टोसाइक्लिन 500ppm"], "mr": ["स्ट्रेप्टोसायक्लिन 500ppm"]}},
                "prevention": {"en": ["Use resistant varieties (e.g., IR64, Swarna)", "Avoid excess nitrogen fertilization", "Maintain proper water management", "Use certified seeds"], "hi": ["प्रतिरोधी किस्में उपयोग करें (जैसे IR64, स्वर्णा)"], "mr": ["प्रतिरोधक जाती वापरा (उदा. IR64, स्वर्णा)"]},
                "severity_info": {"high": {"en": "Apply antibiotic treatment immediately.", "hi": "तुरंत एंटीबायोटिक उपचार लागू करें।", "mr": "लगेच प्रतिजैविक उपचार करा."}, "moderate": {"en": "Isolate and treat affected areas.", "hi": "प्रभावित क्षेत्रों को अलग करें और उपचार करें।", "mr": "प्रभावित भाग वेगळे करा आणि उपचार करा."}, "low": {"en": "Monitor and maintain field hygiene.", "hi": "निगरानी करें और खेत की स्वच्छता बनाए रखें।", "mr": "निरीक्षण करा आणि शेत स्वच्छता राखा."}},
            },
            "rice_healthy": {
                "name": {"en": "Healthy", "hi": "स्वस्थ", "mr": "निरोगी"},
                "crop": "Rice",
                "description": {"en": "Plant appears healthy.", "hi": "पौधा स्वस्थ दिखता है।", "mr": "रोप निरोगी दिसते."},
                "symptoms": {"en": ["No symptoms"], "hi": ["कोई लक्षण नहीं"], "mr": ["कोणतेही लक्षण नाही"]},
                "causes": {"en": ["N/A"], "hi": ["N/A"], "mr": ["N/A"]},
                "treatment": {"organic": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}, "chemical": {"en": ["No treatment needed"], "hi": ["कोई उपचार नहीं"], "mr": ["उपचार नाही"]}},
                "prevention": {"en": ["Continue regular care"], "hi": ["नियमित देखभाल जारी रखें"], "mr": ["नियमित काळजी चालू ठेवा"]},
                "severity_info": {"high": None, "moderate": None, "low": None},
            },
        }
        self._knowledge_base.update(additional)

    def get_disease_info(self, disease_id: str) -> Optional[Dict]:
        """Get full disease information by disease ID."""
        return self._knowledge_base.get(disease_id)

    def get_disease_info_by_class(self, class_name: str) -> Optional[Dict]:
        """
        Get disease info by model class name (e.g., 'Tomato___Early_blight').
        Handles PlantVillage naming conventions including parenthetical qualifiers
        like 'Corn_(maize)' and 'Cherry_(including_sour)'.
        """
        import re

        # Convert: "Tomato___Early_blight" → "tomato_early_blight"
        disease_id = class_name.lower().replace("___", "_").replace(" ", "_")

        # Try direct match first
        if disease_id in self._knowledge_base:
            return self._knowledge_base[disease_id]

        # Strip parenthetical qualifiers: "corn_(maize)_healthy" → "corn_healthy"
        stripped_id = re.sub(r'_?\([^)]*\)_?', '_', disease_id).strip('_')
        if stripped_id in self._knowledge_base:
            return self._knowledge_base[stripped_id]

        # Try with double underscores collapsed
        collapsed = re.sub(r'_+', '_', stripped_id)
        if collapsed in self._knowledge_base:
            return self._knowledge_base[collapsed]

        # Splitting logic to prevent cross-crop matching
        if "___" in class_name:
            crop_part, disease_part = class_name.split("___", 1)
        else:
            parts = class_name.split("_", 1)
            crop_part = parts[0]
            disease_part = parts[1] if len(parts) > 1 else ""

        def clean_string(s: str) -> str:
            return re.sub(r'[^a-z0-9_\s]', '', s.lower())

        crop_clean = clean_string(crop_part).replace("_", " ").strip()
        crop_first_word = crop_clean.split(" ")[0]
        disease_clean = clean_string(disease_part).replace("_", " ").strip()

        # Filter KB keys by crop prefix to avoid cross-crop matches
        crop_prefix = f"{crop_first_word}_"
        possible_keys = [k for k in self._knowledge_base.keys() if k.startswith(crop_prefix)]

        if not possible_keys:
            return None

        # Check if kb_id matches part of the disease_clean or vice versa
        # (e.g. "grape_esca" with "esca black measles")
        for k in possible_keys:
            kb_disease_part = k[len(crop_prefix):]
            kb_disease_clean = kb_disease_part.replace('_', ' ')
            if kb_disease_clean in disease_clean or disease_clean in kb_disease_clean:
                return self._knowledge_base[k]

        # If "healthy" is in the disease name, find the healthy key
        if "healthy" in disease_clean:
            for k in possible_keys:
                if "healthy" in k:
                    return self._knowledge_base[k]

        # Find the key with the highest overlap of words, tie-break by shorter key length
        disease_words = set(disease_clean.split())
        best_key = None
        max_overlap = -1

        for k in possible_keys:
            kb_disease_part = k[len(crop_prefix):].replace("_", " ")
            kb_words = set(kb_disease_part.split())
            overlap = len(disease_words.intersection(kb_words))
            if overlap > max_overlap:
                max_overlap = overlap
                best_key = k
            elif overlap == max_overlap and best_key is not None:
                if len(k) < len(best_key):
                    best_key = k

        if best_key:
            return self._knowledge_base[best_key]

        return None

    def get_supported_crops(self) -> List[str]:
        """Get list of all supported crops."""
        crops = set()
        for info in self._knowledge_base.values():
            crop = info.get("crop", "Unknown")
            crops.add(crop)
        return sorted(list(crops))

    def get_diseases_for_crop(self, crop: str) -> List[Dict]:
        """Get all diseases for a specific crop."""
        results = []
        for disease_id, info in self._knowledge_base.items():
            if info.get("crop", "").lower() == crop.lower():
                results.append({
                    "id": disease_id,
                    "name": info["name"],
                    "crop": info["crop"],
                })
        return results

    def get_dynamic_fallback_info(self, class_name: str, crop: str, lang: str = "en") -> Dict:
        """
        Generates general localized guidelines and treatment recommendations
        for crops/diseases not present in the static database.
        """
        import re
        # Clean crop & disease name for display
        clean_name = class_name.replace("___", " — ").replace("_", " ")
        # Capitalize words
        clean_name = " ".join([w.capitalize() for w in clean_name.split()])

        is_healthy = "healthy" in class_name.lower()

        # Localized templates
        if lang == "hi":
            if is_healthy:
                return {
                    "name": "स्वस्थ पौधा",
                    "crop": crop,
                    "description": f"यह {crop} का पौधा पूरी तरह से स्वस्थ प्रतीत होता है। पत्तियों पर कोई रोग या कीट के लक्षण नहीं दिख रहे हैं।",
                    "symptoms": ["पत्तियाँ प्राकृतिक हरी और चमकदार हैं।", "कोई धब्बे, मुरझाना या विरूपण नहीं है।"],
                    "causes": ["नियमित देखभाल और अनुकूल मौसम।", "उचित सिंचाई और संतुलित पोषण।"],
                    "treatment": {
                        "organic": ["जैविक खाद (वर्मीकंपोस्ट) का नियमित उपयोग जारी रखें।"],
                        "chemical": ["स्वस्थ पौधों के लिए किसी रासायनिक कीटनाशक की आवश्यकता नहीं है।"]
                    },
                    "prevention": [
                        "नियमित रूप से पौधों की निगरानी करते रहें।",
                        "पौधे के आधार पर पानी दें, पत्तियों को गीला करने से बचें।"
                    ],
                    "severity_info": "पौधा पूरी तरह से स्वस्थ है। सामान्य देखभाल जारी रखें।"
                }
            else:
                disease_label = clean_name.split(" — ")[-1] if " — " in clean_name else clean_name
                # Detect disease type
                disease_type = "fungal"
                if any(x in class_name.lower() for x in ["bacteria", "scab"]):
                    disease_type = "bacterial"
                elif any(x in class_name.lower() for x in ["virus", "mosaic"]):
                    disease_type = "viral"
                elif any(x in class_name.lower() for x in ["mite", "insect", "pest"]):
                    disease_type = "pest"

                desc = f"यह {crop} के पौधे पर {disease_label} के संभावित लक्षण हैं। यह एक {disease_type} संक्रमण हो सकता है।"
                symptoms = [
                    "पत्तियों पर असामान्य धब्बे या रंग में बदलाव।",
                    "पत्तियों के किनारों का सूखना या मुड़ना।"
                ]
                organic_treatments = [
                    "संक्रमित पत्तियों और शाखाओं को काटकर नष्ट कर दें ताकि संक्रमण आगे न फैले।",
                    "पौधों पर नीम के तेल (Neem Oil) का छिड़काव करें जो प्राकृतिक कीटनाशक और फंगस रोधी है।"
                ]
                chemical_treatments = []
                if disease_type == "fungal":
                    chemical_treatments.append("फंगल संक्रमण के लिए मैन्कोजेब (Mancozeb) या कॉपर ऑक्सीक्लोराइड का छिड़काव करें।")
                elif disease_type == "bacterial":
                    chemical_treatments.append("जीवाणु संक्रमण के लिए कॉपर-आधारित बैक्टीरिसाइड का उपयोग करें।")
                elif disease_type == "pest":
                    chemical_treatments.append("कीट नियंत्रण के लिए अनुशंसित प्रणालीगत कीटनाशक का छिड़काव करें।")
                else:
                    chemical_treatments.append("लक्षण बढ़ने पर कृषि विशेषज्ञ की सलाह से उपचार चुनें।")

                return {
                    "name": disease_label,
                    "crop": crop,
                    "description": desc,
                    "symptoms": symptoms,
                    "causes": ["अत्यधिक नमी या हवा का कम संचार।", "संक्रमित मिट्टी, पानी या कृषि उपकरण।"],
                    "treatment": {
                        "organic": organic_treatments,
                        "chemical": chemical_treatments
                    },
                    "prevention": [
                        "फसल चक्र (Crop Rotation) अपनाएं।",
                        "पौधों के बीच पर्याप्त दूरी रखें ताकि धूप और हवा सही से मिल सके।"
                    ],
                    "severity_info": "संक्रमित भागों को तुरंत काटकर हटा दें और नमी को नियंत्रित करें।"
                }
        elif lang == "mr":
            if is_healthy:
                return {
                    "name": "निरोगी रोप",
                    "crop": crop,
                    "description": f"हे {crop} चे रोप पूर्णपणे निरोगी दिसत आहे. पानांवर कोणत्याही रोगाची किंवा कीडची लक्षणे दिसत नाहीत.",
                    "symptoms": ["पाने नैसर्गिक हिरवी आणि तजेलदार आहेत.", "पानांवर कोणतेही डाग किंवा वाळण्याची लक्षणे नाहीत."],
                    "causes": ["नियमित काळजी आणि अनुकूल हवामान.", "योग्य पाणी व्यवस्थापन आणि संतुलित पोषण."],
                    "treatment": {
                        "organic": ["नियमित सेंद्रिय खतांचा वापर सुरू ठेवा."],
                        "chemical": ["निरोगी रोपांवर रासायनिक फवारणीची आवश्यकता नाही."]
                    },
                    "prevention": [
                        "रोपांचे नियमित निरीक्षण करत राहा.",
                        "पाणी देताना ते पानांवर न टाकता थेट मुळाशी द्या."
                    ],
                    "severity_info": "रोप निरोगी आहे. नियमित काळजी घ्या."
                }
            else:
                disease_label = clean_name.split(" — ")[-1] if " — " in clean_name else clean_name
                disease_type = "fungal"
                if any(x in class_name.lower() for x in ["bacteria", "scab"]):
                    disease_type = "bacterial"
                elif any(x in class_name.lower() for x in ["virus", "mosaic"]):
                    disease_type = "viral"
                elif any(x in class_name.lower() for x in ["mite", "insect", "pest"]):
                    disease_type = "pest"

                desc = f"हे {crop} च्या रोपावर {disease_label} चे संभाव्य लक्षण आहे. हा {disease_type} संसर्ग असू शकतो."
                symptoms = [
                    "पानांवर असामान्य डाग किंवा रंग बदलणे.",
                    "पाने आकसणे किंवा वाळणे."
                ]
                organic_treatments = [
                    "बाधित पाने आणि फांद्या त्वरित कापून नष्ट करा जेणेकरून रोग पसरणार नाही.",
                    "प्रतिबंधक उपाय म्हणून कडुनिंबाच्या अर्काची (Neem Oil) फवारणी करा."
                ]
                chemical_treatments = []
                if disease_type == "fungal":
                    chemical_treatments.append("बुरशीजन्य रोगांसाठी मॅन्कोझेब (Mancozeb) किंवा कॉपर ऑक्सिक्लोराईड बुरशीनाशकाची फवारणी करा.")
                elif disease_type == "bacterial":
                    chemical_treatments.append("जीवाणू संसर्गासाठी तांबेयुक्त जिवाणूनाशकाचा वापर करा.")
                elif disease_type == "pest":
                    chemical_treatments.append("कीड नियंत्रणासाठी शिफारस केलेल्या कीटकनाशकाची फवारणी करा.")
                else:
                    chemical_treatments.append("कृषी तज्ज्ञांच्या सल्ल्याने योग्य फवारणी करा.")

                return {
                    "name": disease_label,
                    "crop": crop,
                    "description": desc,
                    "symptoms": symptoms,
                    "causes": ["अति आर्द्रता किंवा हवेचा अभाव.", "बाधित माती, पाणी किंवा अवजारे."],
                    "treatment": {
                        "organic": organic_treatments,
                        "chemical": chemical_treatments
                    },
                    "prevention": [
                        "पिकांची फेरपालट करा.",
                        "रोपांमध्ये योग्य अंतर ठेवा जेणेकरून खेळती हवा राहील."
                    ],
                    "severity_info": "बाधित भाग काढून टाका आणि पाणी देणे मर्यादित करा."
                }
        else: # English
            if is_healthy:
                return {
                    "name": "Healthy",
                    "crop": crop,
                    "description": f"This {crop} plant appears completely healthy with no visible signs of pests or disease.",
                    "symptoms": ["Leaves are vibrant and green.", "No spots, wilting, or leaf curling."],
                    "causes": ["Proper irrigation, balanced soil nutrients, and good crop management."],
                    "treatment": {
                        "organic": ["Continue regular organic fertilization (compost/manure)."],
                        "chemical": ["No chemical treatments or sprays are needed for healthy plants."]
                    },
                    "prevention": [
                        "Monitor plants regularly for early signs of pest activity.",
                        "Water at the base of the plant to keep the foliage dry."
                    ],
                    "severity_info": "The plant is healthy. Continue normal cultivation practices."
                }
            else:
                disease_label = clean_name.split(" — ")[-1] if " — " in clean_name else clean_name
                disease_type = "fungal"
                if any(x in class_name.lower() for x in ["bacteria", "scab"]):
                    disease_type = "bacterial"
                elif any(x in class_name.lower() for x in ["virus", "mosaic"]):
                    disease_type = "viral"
                elif any(x in class_name.lower() for x in ["mite", "insect", "pest"]):
                    disease_type = "pest"

                desc = f"Possible signs of {disease_label} observed on this {crop} plant. It likely indicates a {disease_type} infection."
                symptoms = [
                    "Irregular lesions or discoloration on leaves.",
                    "Yellowing or curling of leaf edges."
                ]
                organic_treatments = [
                    "Prune and destroy infected plant parts immediately to reduce inoculum spread.",
                    "Apply Neem Oil or bio-fungicides to control early infestations organically."
                ]
                chemical_treatments = []
                if disease_type == "fungal":
                    chemical_treatments.append("Apply broad-spectrum fungicides such as Mancozeb or Chlorothalonil.")
                elif disease_type == "bacterial":
                    chemical_treatments.append("Use copper-based bactericides or copper oxychloride sprays.")
                elif disease_type == "pest":
                    chemical_treatments.append("Apply recommended systemic insecticides or miticides.")
                else:
                    chemical_treatments.append("Consult an agricultural specialist if symptoms worsen.")

                return {
                    "name": disease_label,
                    "crop": crop,
                    "description": desc,
                    "symptoms": symptoms,
                    "causes": ["High humidity or poor air circulation.", "Contaminated soil, water, or tools."],
                    "treatment": {
                        "organic": organic_treatments,
                        "chemical": chemical_treatments
                    },
                    "prevention": [
                        "Practice crop rotation to break disease cycles.",
                        "Ensure proper plant spacing for sunlight and air flow."
                    ],
                    "severity_info": "Isolate or prune infected parts, reduce overhead watering, and monitor closely."
                }
