"""
Agronomic Knowledge Base for AI Crop Disease Prediction & Management System.
Covers 15 crop species and all 41 canonical disease profiles with bioclimatic triggers,
scientifically validated organic remedies, approved chemical controls (with PHI), and cultural management.
"""

import copy

CROPS_DATABASE = {
    "Tomato": {
        "icon": "🍅",
        "scientific_name": "Solanum lycopersicum",
        "diseases": [
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Bacterial_spot",
            "Tomato___Septoria_leaf_spot",
            "Tomato___Target_Spot",
            "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
            "Tomato___Tomato_mosaic_virus",
            "Tomato___Spider_mites Two-spotted_spider_mite",
            "Tomato___Leaf_Mold",
            "Tomato___healthy"
        ]
    },
    "Potato": {
        "icon": "🥔",
        "scientific_name": "Solanum tuberosum",
        "diseases": [
            "Potato___Early_blight",
            "Potato___Late_blight",
            "Potato___healthy"
        ]
    },
    "Corn (Maize)": {
        "icon": "🌽",
        "scientific_name": "Zea mays",
        "diseases": [
            "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
            "Corn_(maize)___Common_rust_",
            "Corn_(maize)___Northern_Leaf_Blight",
            "Corn_(maize)___healthy"
        ]
    },
    "Apple": {
        "icon": "🍎",
        "scientific_name": "Malus domestica",
        "diseases": [
            "Apple___Apple_scab",
            "Apple___Black_rot",
            "Apple___Cedar_apple_rust",
            "Apple___healthy"
        ]
    },
    "Grape": {
        "icon": "🍇",
        "scientific_name": "Vitis vinifera",
        "diseases": [
            "Grape___Black_rot",
            "Grape___Esca_(Black_Measles)",
            "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
            "Grape___healthy"
        ]
    },
    "Bell Pepper": {
        "icon": "🫑",
        "scientific_name": "Capsicum annuum",
        "diseases": [
            "Pepper,_bell___Bacterial_spot",
            "Pepper,_bell___healthy"
        ]
    },
    "Rice / Paddy": {
        "icon": "🌾",
        "scientific_name": "Oryza sativa",
        "diseases": [
            "Rice___Bacterial_leaf_blight",
            "Rice___Brown_spot",
            "Rice___Leaf_blast",
            "Rice___Leaf_smut",
            "Rice___healthy"
        ]
    },
    "Blueberry": {
        "icon": "🫐",
        "scientific_name": "Vaccinium corymbosum",
        "diseases": [
            "Blueberry___healthy"
        ]
    },
    "Cherry": {
        "icon": "🍒",
        "scientific_name": "Prunus avium",
        "diseases": [
            "Cherry_(including_sour)___Powdery_mildew",
            "Cherry_(including_sour)___healthy"
        ]
    },
    "Orange": {
        "icon": "🍊",
        "scientific_name": "Citrus sinensis",
        "diseases": [
            "Orange___Haunglongbing_(Citrus_greening)"
        ]
    },
    "Peach": {
        "icon": "🍑",
        "scientific_name": "Prunus persica",
        "diseases": [
            "Peach___Bacterial_spot",
            "Peach___healthy"
        ]
    },
    "Raspberry": {
        "icon": "🍇",
        "scientific_name": "Rubus idaeus",
        "diseases": [
            "Raspberry___healthy"
        ]
    },
    "Soybean": {
        "icon": "🌱",
        "scientific_name": "Glycine max",
        "diseases": [
            "Soybean___healthy"
        ]
    },
    "Squash": {
        "icon": "🎃",
        "scientific_name": "Cucurbita pepo",
        "diseases": [
            "Squash___Powdery_mildew"
        ]
    },
    "Strawberry": {
        "icon": "🍓",
        "scientific_name": "Fragaria ananassa",
        "diseases": [
            "Strawberry___Leaf_scorch",
            "Strawberry___healthy"
        ]
    }
}

DISEASE_PROFILES = {
    # ------------------ TOMATO (10) ------------------
    "Tomato___Late_blight": {
        "common_name": "Tomato Late Blight",
        "crop": "Tomato",
        "pathogen_type": "Oomycete / Water Mold",
        "causal_agent": "Phytophthora infestans",
        "severity_level": "Critical",
        "symptoms": [
            "Large, irregular water-soaked greenish-black lesions on leaves",
            "White fuzzy sporulation on leaf undersides in high humidity",
            "Dark brown blotches on stems and firm greasy lesions on fruits",
            "Rapid foliage collapse within 48-72 hours under cool, wet conditions"
        ],
        "bioclimatic_triggers": {
            "temp_min": 10.0, "temp_optimal_min": 15.0, "temp_optimal_max": 22.0, "temp_max": 26.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "High (continuous rain/fog)", "soil_moisture_risk": "High saturation"
        },
        "management": {
            "preventive_intervention": [
                "Ensure wide plant spacing (60-75 cm) for canopy aeration",
                "Use drip irrigation to prevent foliage wetting",
                "Rogue out and destroy infected volunteer solanaceous plants"
            ],
            "organic_controls": [
                {"name": "Copper Hydroxide / Copper Octanoate", "dosage": "2.5 g per Liter water", "frequency": "Every 7 days in high humidity", "phi_days": 1},
                {"name": "Bacillus subtilis Bio-fungicide", "dosage": "5-10 g per Liter water", "frequency": "Every 5-7 days preventively", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP (Contact Protectant)", "dosage": "2.5 g per Liter water", "frequency": "Every 7-10 days preventively", "phi_days": 7},
                {"name": "Dimethomorph 50% + Cymoxanil (Curative/Systemic)", "dosage": "1.5 g per Liter water", "frequency": "Apply immediately at onset", "phi_days": 5}
            ],
            "cultural_practices": "Prune lower leaves touching soil; mulch surface to avoid soil splash."
        }
    },
    "Tomato___Early_blight": {
        "common_name": "Tomato Early Blight",
        "crop": "Tomato",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "severity_level": "High",
        "symptoms": [
            "Circular brown-black spots with concentric target-like rings on older leaves",
            "Chlorotic yellow halos surrounding necrotic lesions",
            "Gradual defoliation progressing upwards from lower canopy",
            "Sunscald vulnerability on exposed fruits"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 29.0, "temp_max": 34.0,
            "humidity_threshold": 80.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Stake plants and prune bottom 30 cm foliage to prevent soil splash",
                "Rotate with non-solanaceous crops on a 2-3 year cycle",
                "Avoid overhead sprinkler irrigation"
            ],
            "organic_controls": [
                {"name": "Trichoderma harzianum Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Every 10 days preventively", "phi_days": 0},
                {"name": "Neem Seed Kernel Extract (NSKE 5%)", "dosage": "50 ml per Liter water", "frequency": "Every 7-10 days", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Chlorothalonil 75% WP (Protectant)", "dosage": "2.0 g per Liter water", "frequency": "Every 7-10 days", "phi_days": 7},
                {"name": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC", "dosage": "1.0 ml per Liter water", "frequency": "Apply at first lesion", "phi_days": 5}
            ],
            "cultural_practices": "Burn or deeply bury infected crop residue immediately after harvest."
        }
    },
    "Tomato___Bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas perforans / euvesicatoria",
        "severity_level": "High",
        "symptoms": [
            "Small (1-3 mm), dark, greasy or water-soaked spots on leaves",
            "Lesion centers dry out and drop out, creating a shot-hole appearance",
            "Raised, scabby spots with warty halos on green fruits",
            "Severe leaf drop in warm, rainy weather leading to fruit scald"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0, "temp_optimal_min": 25.0, "temp_optimal_max": 32.0, "temp_max": 36.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 5.0,
            "rainfall_risk": "High (wind-driven rain)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Use certified disease-free, hot-water-treated seeds",
                "Sanitize stakes, pruning knives, and hands between plants",
                "Never work or cultivate in wet fields to prevent bacterial spread"
            ],
            "organic_controls": [
                {"name": "Copper Oxychloride 50% WP (Fixed Copper)", "dosage": "2.5 g per Liter water", "frequency": "Every 7 days in wet weather", "phi_days": 1},
                {"name": "Bacillus amyloliquefaciens Bio-bactericide", "dosage": "5 g per Liter water", "frequency": "Preventive weekly spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Copper Hydroxide 53.8% DF + Kasugamycin / Streptocycline", "dosage": "2.0 g Copper + 0.1 g Streptocycline per L", "frequency": "Apply preventively in wet conditions", "phi_days": 3}
            ],
            "cultural_practices": "Bacterial disease cannot be controlled by synthetic fungicides like Mancozeb; focus on copper bactericides and strict sanitation."
        }
    },
    "Tomato___Leaf_Mold": {
        "common_name": "Tomato Leaf Mold",
        "crop": "Tomato",
        "pathogen_type": "Fungal",
        "causal_agent": "Passalora fulva (syn. Cladosporium fulvum)",
        "severity_level": "Moderate",
        "symptoms": [
            "Pale green to yellowish spots on upper leaf surfaces with indistinct margins",
            "Dense olive-green to brownish velvety fungal growth on lower leaf surfaces",
            "Older leaves wither, curl, and die prematurely",
            "Common in protected greenhouses and dense, poorly ventilated canopies"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 21.0, "temp_optimal_max": 25.0, "temp_max": 30.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Low to Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Increase greenhouse ventilation and air circulation fans",
                "Keep relative humidity strictly below 85%",
                "Remove and bag affected bottom foliage"
            ],
            "organic_controls": [
                {"name": "Potassium Bicarbonate Fungicide", "dosage": "3 g per Liter water", "frequency": "Every 7 days", "phi_days": 0},
                {"name": "Neem Oil 10,000 PPM", "dosage": "5 ml per Liter water", "frequency": "Every 7-10 days", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Difenoconazole 25% EC", "dosage": "0.5 ml per Liter water", "frequency": "Every 10-14 days", "phi_days": 7}
            ],
            "cultural_practices": "Heat greenhouses slightly at night with ridge vents open to prevent dew formation on leaves."
        }
    },
    "Tomato___Septoria_leaf_spot": {
        "common_name": "Tomato Septoria Leaf Spot",
        "crop": "Tomato",
        "pathogen_type": "Fungal",
        "causal_agent": "Septoria lycopersici",
        "severity_level": "Moderate",
        "symptoms": [
            "Numerous circular spots (1.5-3 mm) with dark brown margins and grey/tan centers",
            "Tiny black specks (pycnidia) visible inside mature lesion centers",
            "Progressive yellowing and defoliation from bottom of canopy upward",
            "Stems and petioles show similar small circular lesions"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 20.0, "temp_optimal_max": 26.0, "temp_max": 30.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "High (rain splash)", "soil_moisture_risk": "High"
        },
        "management": {
            "preventive_intervention": [
                "Avoid overhead irrigation to minimize leaf moisture duration",
                "Mulch heavily around base of plants with straw or plastic",
                "Maintain 3-year crop rotation away from solanaceous plants"
            ],
            "organic_controls": [
                {"name": "Copper Soap (Copper Octanoate)", "dosage": "2 g per Liter water", "frequency": "Every 7-10 days", "phi_days": 1},
                {"name": "Bio-fungicide (Trichoderma viride)", "dosage": "5 g per Liter water", "frequency": "Preventive foliar spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Chlorothalonil 75% WP", "dosage": "2.0 g per Liter water", "frequency": "Every 7-10 days", "phi_days": 7},
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Every 10-12 days", "phi_days": 7}
            ],
            "cultural_practices": "Strip lower leaves as tomato vines grow to maintain 30 cm ground clearance."
        }
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "common_name": "Two-Spotted Spider Mite Infestation",
        "crop": "Tomato",
        "pathogen_type": "Mite / Vector-borne Pest",
        "causal_agent": "Tetranychus urticae",
        "severity_level": "Moderate",
        "symptoms": [
            "Fine pale-yellow stippling or bronzing on upper leaf surfaces",
            "Fine silken webbing on undersides of leaves and growing tips",
            "Leaves turn yellow, dry, brittle, and drop off prematurely",
            "Severe infestation leads to total plant chlorosis and webbing over flowers"
        ],
        "bioclimatic_triggers": {
            "temp_min": 22.0, "temp_optimal_min": 28.0, "temp_optimal_max": 36.0, "temp_max": 42.0,
            "humidity_threshold": 40.0, "leaf_wetness_hours_threshold": 1.0,
            "rainfall_risk": "Very Low (favored by hot, dry conditions)", "soil_moisture_risk": "Low"
        },
        "management": {
            "preventive_intervention": [
                "Control field dust by watering farm roadways (dust favors mite outbreaks)",
                "Avoid excessive nitrogen fertilization which increases mite fecundity",
                "Overhead misting can disrupt mite reproduction in dry seasons"
            ],
            "organic_controls": [
                {"name": "Horticultural Mineral Oil / Insecticidal Soap", "dosage": "10 ml per Liter water", "frequency": "Thorough canopy spray every 5 days", "phi_days": 0},
                {"name": "Neem Oil (Azadirachtin 1%)", "dosage": "4 ml per Liter water", "frequency": "Every 7 days", "phi_days": 0},
                {"name": "Predatory Mites (Phytoseiulus persimilis)", "dosage": "Biological release per canopy area", "frequency": "Introduce at first stippling", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Spiromesifen 22.9% SC (Acaricide)", "dosage": "1.0 ml per Liter water", "frequency": "Apply once; rotate mode of action", "phi_days": 3},
                {"name": "Abamectin 1.9% EC (Miticide)", "dosage": "0.5 ml per Liter water", "frequency": "Thorough underside coverage", "phi_days": 7}
            ],
            "cultural_practices": "Spider mites are arachnid pests, NOT fungal or bacterial pathogens. Never apply broad-spectrum pyrethroids as they kill natural predatory mites."
        }
    },
    "Tomato___Target_Spot": {
        "common_name": "Tomato Target Spot",
        "crop": "Tomato",
        "pathogen_type": "Fungal",
        "causal_agent": "Corynespora cassiicola",
        "severity_level": "High",
        "symptoms": [
            "Pinpoint brown spots that expand into circular brown lesions with light brown centers",
            "Zonate concentric rings that can resemble early blight lesions",
            "Lesions rapidly coalesce causing extensive leaf blighting and defoliation",
            "Depressed brown circular lesions with dark margins on fruits"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 25.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 80.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate to High", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Maintain wide spacing and stake plants to improve ventilation",
                "Avoid overhead irrigation",
                "Eradicate weed hosts such as nightshades and wild legumes"
            ],
            "organic_controls": [
                {"name": "Copper Hydroxide 50% WP", "dosage": "2.0 g per Liter water", "frequency": "Every 7-10 days", "phi_days": 1},
                {"name": "Bio-control (Bacillus subtilis)", "dosage": "5 g per Liter water", "frequency": "Preventive spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Azoxystrobin 23% SC", "dosage": "1.0 ml per Liter water", "frequency": "Every 10-14 days", "phi_days": 3},
                {"name": "Boscalid + Pyraclostrobin WG", "dosage": "1.0 g per Liter water", "frequency": "Rotate with contact fungicides", "phi_days": 4}
            ],
            "cultural_practices": "Remove lower diseased foliage immediately; sanitize tools after field work."
        }
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "common_name": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "crop": "Tomato",
        "pathogen_type": "Viral",
        "causal_agent": "Begomovirus (vectored by Silverleaf Whitefly, Bemisia tabaci)",
        "severity_level": "Critical",
        "symptoms": [
            "Marked upward cupping and curling of leaf margins into cup shapes",
            "Severe interveinal chlorosis (yellowing) with stunted small leaflets",
            "Extreme stunting of plant internodes creating a bushy top appearance",
            "Flowers abort and drop off; virtually no fruit set if infected early"
        ],
        "bioclimatic_triggers": {
            "temp_min": 22.0, "temp_optimal_min": 28.0, "temp_optimal_max": 36.0, "temp_max": 42.0,
            "humidity_threshold": 45.0, "leaf_wetness_hours_threshold": 1.0,
            "rainfall_risk": "Low (dry weather accelerates whitefly proliferation)", "soil_moisture_risk": "Low to Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Install yellow sticky traps (10-15 traps per acre) to monitor and mass-trap whiteflies",
                "Grow TYLCV-resistant hybrids (e.g. Ty-1 / Ty-3 resistance genes)",
                "Protect nursery beds with 40-50 mesh insect-proof netting"
            ],
            "organic_controls": [
                {"name": "Neem Oil 10,000 PPM / NSKE 5%", "dosage": "5 ml per Liter water", "frequency": "Every 5-7 days for whitefly vector suppression", "phi_days": 0},
                {"name": "Beauveria bassiana Entomopathogenic Bio-pesticide", "dosage": "5 g per Liter water", "frequency": "Foliar spray targeted at nymphs", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Thiamethoxam 25% WG (Systemic Vector Control)", "dosage": "0.3 g per Liter water", "frequency": "Seedling drench or early foliar spray", "phi_days": 5},
                {"name": "Diafenthiuron 50% WP (Vector suppression)", "dosage": "1.2 g per Liter water", "frequency": "At economic threshold (>5 whiteflies/leaf)", "phi_days": 7}
            ],
            "cultural_practices": "VIRAL INFECTION CANNOT BE CURED. Chemical fungicides have ZERO efficacy. Promptly rogue out and destroy symptomatic plants to prevent vector transmission to healthy rows."
        }
    },
    "Tomato___Tomato_mosaic_virus": {
        "common_name": "Tomato Mosaic Virus (ToMV)",
        "crop": "Tomato",
        "pathogen_type": "Viral",
        "causal_agent": "Tobamovirus (mechanically transmitted via hands, tools, and seeds)",
        "severity_level": "High",
        "symptoms": [
            "Mottling of leaves with alternating light and dark green mosaic patterns",
            "Leaf distortion, blistering, and 'shoestring' narrowing of leaf blades",
            "Internal brown necrotic rings (browning) inside ripe fruits",
            "General plant stunting and reduced yield"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 30.0, "temp_max": 38.0,
            "humidity_threshold": 50.0, "leaf_wetness_hours_threshold": 1.0,
            "rainfall_risk": "Low", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Dip tools and hands in 10% non-fat dry milk solution or 20% trisodium phosphate during handling",
                "Prohibit tobacco use (smoking/chewing) near plants as tobacco carries related tobamoviruses",
                "Use certified virus-free seed treated with 10% trisodium phosphate"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "VIRAL INFECTION CANNOT BE TREATED WITH CHEMICALS. Fungicides are completely ineffective. Remove and incinerate infected plants. Disinfect stakes and greenhouse surfaces with 10% bleach."
        }
    },
    "Tomato___healthy": {
        "common_name": "Healthy Tomato",
        "crop": "Tomato",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Vibrant green, uniform foliage with well-defined leaf margins",
            "Zero active necrotic lesions, water-soaked spots, or viral curling",
            "Strong vegetative vigor, healthy blossoms, and uniform fruit set"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 22.0, "temp_optimal_max": 28.0, "temp_max": 32.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Optimal", "soil_moisture_risk": "Field capacity"
        },
        "management": {
            "preventive_intervention": [
                "Maintain consistent soil moisture through regular drip irrigation",
                "Apply balanced N-P-K fertilizer with adequate calcium to prevent blossom end rot",
                "Scout weekly for early signs of hornworms, mites, or leaf spots"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No pesticide or fungicide intervention is required. Maintain good sanitation and weed-free borders."
        }
    },

    # ------------------ POTATO (3) ------------------
    "Potato___Late_blight": {
        "common_name": "Potato Late Blight",
        "crop": "Potato",
        "pathogen_type": "Oomycete / Water Mold",
        "causal_agent": "Phytophthora infestans",
        "severity_level": "Critical",
        "symptoms": [
            "Irregular, dark water-soaked spots on leaf tips and margins",
            "White fungal-like mildew on undersides of leaves under cool, humid weather",
            "Stems develop dark brown lesions, leading to vine collapse",
            "Tubers develop purplish-brown surface discoloration and granular dry rot inside"
        ],
        "bioclimatic_triggers": {
            "temp_min": 10.0, "temp_optimal_min": 14.0, "temp_optimal_max": 20.0, "temp_max": 24.0,
            "humidity_threshold": 88.0, "leaf_wetness_hours_threshold": 10.0,
            "rainfall_risk": "High (fog, drizzle, overcast)", "soil_moisture_risk": "High"
        },
        "management": {
            "preventive_intervention": [
                "Plant certified disease-free seed tubers",
                "Hill soil well over tubers (at least 10-15 cm) to prevent spore washdown",
                "Kill potato vines 2 weeks before harvest to prevent tuber contamination at digging"
            ],
            "organic_controls": [
                {"name": "Copper Oxychloride 50% WP", "dosage": "2.5 g per Liter water", "frequency": "Preventive spray before rain events", "phi_days": 1},
                {"name": "Trichoderma viride Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Soil application at planting", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Every 7 days preventively", "phi_days": 7},
                {"name": "Cymoxanil 8% + Mancozeb 64% WP", "dosage": "2.0 g per Liter water", "frequency": "Apply immediately upon early warning", "phi_days": 7},
                {"name": "Metalaxyl-M 4% + Mancozeb 64% WP", "dosage": "2.5 g per Liter water", "frequency": "Maximum 2 systemic applications per season", "phi_days": 14}
            ],
            "cultural_practices": "Destroy cull piles; never leave diseased tubers on the field surface."
        }
    },
    "Potato___Early_blight": {
        "common_name": "Potato Early Blight",
        "crop": "Potato",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "severity_level": "High",
        "symptoms": [
            "Dark brown to black lesions with concentric rings (target spots) on leaves",
            "Yellow chlorotic halos surrounding lesions",
            "Premature senescence of lower canopy leaves",
            "Dark, sunken, leathery lesions on tuber skins"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 29.0, "temp_max": 33.0,
            "humidity_threshold": 78.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Maintain optimal crop nutrition; plants stressed for nitrogen are far more vulnerable",
                "Ensure proper crop rotation away from solanaceous species for 2-3 years",
                "Avoid overhead sprinkler irrigation late in the day"
            ],
            "organic_controls": [
                {"name": "Neem Oil 10,000 PPM", "dosage": "5 ml per Liter water", "frequency": "Every 7-10 days", "phi_days": 0},
                {"name": "Bacillus subtilis Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Foliar spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Every 7-10 days", "phi_days": 7},
                {"name": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC", "dosage": "1.0 ml per Liter water", "frequency": "At onset of symptoms", "phi_days": 7}
            ],
            "cultural_practices": "Disinfect storage bins before loading potato tubers; maintain tubers at 10-15°C for 2 weeks to heal skin abrasions."
        }
    },
    "Potato___healthy": {
        "common_name": "Healthy Potato",
        "crop": "Potato",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Sturdy green haulms with lush, uniform foliage",
            "Absence of water-soaked blights or target spot necrosis",
            "Vigorous stolon development and uniform tuber bulking"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 18.0, "temp_optimal_max": 22.0, "temp_max": 26.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Optimal", "soil_moisture_risk": "Adequate"
        },
        "management": {
            "preventive_intervention": [
                "Maintain uniform soil moisture during tuber initiation and bulking",
                "Hill potato rows regularly to protect expanding tubers from greening and pests",
                "Scout weekly for Colorado potato beetles and early blight lesions"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No chemical fungicide application required. Maintain field borders and soil aeration."
        }
    },

    # ------------------ CORN / MAIZE (4) ------------------
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "common_name": "Corn Gray Leaf Spot",
        "crop": "Corn (Maize)",
        "pathogen_type": "Fungal",
        "causal_agent": "Cercospora zeae-maydis",
        "severity_level": "High",
        "symptoms": [
            "Tan to gray rectangular lesions strictly bounded by leaf veins",
            "Lesions expand to 2-7 cm length creating a blocky striped appearance",
            "Severe blighting of whole leaf canopy leading to lodging and reduced ear fill",
            "Gray velvety fungal sporulation on lesions during morning dew"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0, "temp_optimal_min": 25.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 90.0, "leaf_wetness_hours_threshold": 10.0,
            "rainfall_risk": "Moderate to High", "soil_moisture_risk": "High"
        },
        "management": {
            "preventive_intervention": [
                "Select corn hybrids with high resistance scores to Gray Leaf Spot",
                "Rotate with non-host crops (soybeans, sorghum, pulses) for 1-2 years",
                "Incorporate crop residue with tillage where conservation practices permit"
            ],
            "organic_controls": [
                {"name": "Trichoderma harzianum Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Preventive foliar application", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC", "dosage": "1.0 ml per Liter water", "frequency": "Apply between tasseling (VT) and silking (R1)", "phi_days": 14},
                {"name": "Pyraclostrobin 20% WG", "dosage": "1.0 g per Liter water", "frequency": "At first sign on third leaf below ear", "phi_days": 14}
            ],
            "cultural_practices": "Avoid high planting densities that restrict airflow in the canopy."
        }
    },
    "Corn_(maize)___Common_rust_": {
        "common_name": "Corn Common Rust",
        "crop": "Corn (Maize)",
        "pathogen_type": "Fungal",
        "causal_agent": "Puccinia sorghi",
        "severity_level": "Moderate",
        "symptoms": [
            "Oval to elongate cinnamon-brown powdery pustules on both upper and lower leaf surfaces",
            "Pustules rupture the leaf epidermis, releasing reddish-brown urediniospores",
            "As season progresses, pustules turn brownish-black with teliospores",
            "Heavily infected leaves turn yellow, senesce, and dry out"
        ],
        "bioclimatic_triggers": {
            "temp_min": 14.0, "temp_optimal_min": 18.0, "temp_optimal_max": 24.0, "temp_max": 28.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "High (frequent rain and cool nights)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Plant rust-resistant corn hybrids carrying Rp gene resistance",
                "Plant early in the season to avoid late-season airborne spore showers",
                "Maintain balanced soil fertility without excessive late nitrogen"
            ],
            "organic_controls": [
                {"name": "Wettable Sulfur 80% WDG", "dosage": "3 g per Liter water", "frequency": "At first pustule sighting", "phi_days": 3}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Apply early when pustules appear", "phi_days": 14},
                {"name": "Tebuconazole 25.9% EC", "dosage": "1.0 ml per Liter water", "frequency": "Apply prior to silking if rust exceeds threshold", "phi_days": 21}
            ],
            "cultural_practices": "Common rust thrives in cooler temperatures; scout early planted sweet corn closely."
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "common_name": "Corn Northern Leaf Blight (NCLB)",
        "crop": "Corn (Maize)",
        "pathogen_type": "Fungal",
        "causal_agent": "Setosphaeria turcica (anamorph Exserohilum turcicum)",
        "severity_level": "High",
        "symptoms": [
            "Long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 to 15 cm)",
            "Lesions start on lower leaves and progress upward across leaf veins",
            "Dark, olive-green fungal sporulation within lesions under humid conditions",
            "Extensive blighting of foliage reduces photosynthesis during grain filling"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 20.0, "temp_optimal_max": 26.0, "temp_max": 30.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate to High", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Plant NCLB-resistant corn hybrids with Ht gene resistance",
                "Rotate crops with non-gramineous crops (legumes or oilseeds)",
                "Till or shred crop residue to accelerate residue breakdown"
            ],
            "organic_controls": [
                {"name": "Trichoderma harzianum Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Foliar application", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC", "dosage": "1.0 ml per Liter water", "frequency": "Apply at VT/R1 stage if lesions are present", "phi_days": 14},
                {"name": "Propiconazole 25% EC", "dosage": "1.0 ml per Liter water", "frequency": "Apply at early lesion appearance", "phi_days": 14}
            ],
            "cultural_practices": "Fungicide application is most cost-effective when applied between VT (tasseling) and R1 (silking)."
        }
    },
    "Corn_(maize)___healthy": {
        "common_name": "Healthy Corn (Maize)",
        "crop": "Corn (Maize)",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Broad, dark-green arched leaves free from stripes, spots, or pustules",
            "Sturdy stalks with intact brace roots and uniform ear development",
            "Clean silks and uniform kernel development on cobs"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Adequate", "soil_moisture_risk": "Moist, well-drained"
        },
        "management": {
            "preventive_intervention": [
                "Maintain optimal side-dressing of nitrogen at V6 stage",
                "Ensure weed management during critical weed-free period (V1 to V6)",
                "Scout weekly for fall armyworm and stem borers"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No fungicide or bactericide treatment needed. Maintain weed-free row spacing."
        }
    },

    # ------------------ APPLE (4) ------------------
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "crop": "Apple",
        "pathogen_type": "Fungal",
        "causal_agent": "Venturia inaequalis",
        "severity_level": "High",
        "symptoms": [
            "Olive-green to velvety brown-black spots with feathered margins on leaves",
            "Leaves become curled, distorted, and drop prematurely",
            "Corky, scabby brown lesions on fruits that crack and stunt growth",
            "Severely affected trees suffer pre-harvest fruit drop"
        ],
        "bioclimatic_triggers": {
            "temp_min": 12.0, "temp_optimal_min": 17.0, "temp_optimal_max": 23.0, "temp_max": 27.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 9.0,
            "rainfall_risk": "High (Mills infection period)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Shred or sweep fallen leaves in autumn to disrupt overwintering pseudothecia",
                "Spray orchard floor with 5% urea solution in late autumn to speed leaf decay",
                "Prune tree canopy for maximum sunlight penetration and rapid drying"
            ],
            "organic_controls": [
                {"name": "Wettable Sulfur 80% WDG", "dosage": "3-5 g per Liter water", "frequency": "Every 7 days from green tip stage", "phi_days": 1},
                {"name": "Liquid Lime Sulfur", "dosage": "15 ml per Liter water", "frequency": "Dormant / early spring spray", "phi_days": 5}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP (Protectant)", "dosage": "2.5 g per Liter water", "frequency": "Pink bud to petal fall", "phi_days": 14},
                {"name": "Difenoconazole 25% EC (Curative)", "dosage": "0.3 ml per Liter water", "frequency": "Apply within 48-72 hrs of Mills infection event", "phi_days": 14}
            ],
            "cultural_practices": "Plant scab-resistant apple cultivars such as Prima, Priscilla, or Liberty where feasible."
        }
    },
    "Apple___Black_rot": {
        "common_name": "Apple Black Rot (Frogeye Leaf Spot)",
        "crop": "Apple",
        "pathogen_type": "Fungal",
        "causal_agent": "Botryosphaeria obtusa",
        "severity_level": "High",
        "symptoms": [
            "Small purple spots on leaves expanding into circular lesions with tan centers (frogeye appearance)",
            "Firm, brown rot on fruit expanding in concentric rings of alternating dark and light brown",
            "Fruit eventually turns coal-black, mummifies, and clings to branches",
            "Sunken reddish-brown cankers on limbs and trunks"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 24.0, "temp_optimal_max": 29.0, "temp_max": 32.0,
            "humidity_threshold": 80.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "Moderate to High", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Prune out dead wood, fire blight strikes, and cankered limbs during dormant season",
                "Remove all mummified fruit from trees and orchard floor before bud break",
                "Disinfect pruning shears between cuts with 70% alcohol"
            ],
            "organic_controls": [
                {"name": "Copper Hydroxide 50% WP", "dosage": "2.5 g per Liter water", "frequency": "Delayed dormant spray", "phi_days": 14}
            ],
            "chemical_controls": [
                {"name": "Captan 50% WP", "dosage": "2.5 g per Liter water", "frequency": "Petal fall and cover sprays", "phi_days": 7},
                {"name": "Thiophanate-methyl 70% WP", "dosage": "1.0 g per Liter water", "frequency": "Cover sprays at 14-day intervals", "phi_days": 14}
            ],
            "cultural_practices": "Burn or deeply bury all pruned cankered branches to eliminate inoculum sources."
        }
    },
    "Apple___Cedar_apple_rust": {
        "common_name": "Cedar Apple Rust",
        "crop": "Apple",
        "pathogen_type": "Fungal",
        "causal_agent": "Gymnosporangium juniperi-virginianae",
        "severity_level": "Moderate",
        "symptoms": [
            "Bright orange-yellow circular spots on upper apple leaf surfaces",
            "Tiny black pycnia dots appear in centers of spots",
            "Fringed, tube-like aecia structures form on leaf undersides releasing spores",
            "Requires Eastern Red Cedar or Juniper as alternate host to complete life cycle"
        ],
        "bioclimatic_triggers": {
            "temp_min": 12.0, "temp_optimal_min": 16.0, "temp_optimal_max": 22.0, "temp_max": 26.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "High (spring rains release cedar gall spores)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Remove Eastern Red Cedar (Juniperus virginiana) trees within 500-1000 meters of the orchard",
                "Prune off gelatinous brown galls from nearby ornamental junipers in winter",
                "Select resistant cultivars such as Liberty, Enterprise, or RedFree"
            ],
            "organic_controls": [
                {"name": "Wettable Sulfur 80% WDG", "dosage": "4 g per Liter water", "frequency": "Apply during spring rainy periods", "phi_days": 1}
            ],
            "chemical_controls": [
                {"name": "Myclobutanil 10% WP", "dosage": "1.0 g per Liter water", "frequency": "Tight cluster through petal fall", "phi_days": 14},
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "From pink bud stage", "phi_days": 14}
            ],
            "cultural_practices": "Rust cannot spread from apple to apple; infection comes exclusively from juniper galls in spring."
        }
    },
    "Apple___healthy": {
        "common_name": "Healthy Apple",
        "crop": "Apple",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Glossy, dark-green intact apple foliage with serrated margins",
            "Smooth bark on branches and clean spur development",
            "Clean fruit set without scab blemishes, cankers, or frogeye rings"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 18.0, "temp_optimal_max": 24.0, "temp_max": 30.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Well-drained loam"
        },
        "management": {
            "preventive_intervention": [
                "Perform annual dormant pruning to maintain open canopy structure",
                "Thin young fruitlets to one per spur for optimal size and tree vigor",
                "Monitor pheromone traps for codling moth and apple maggot"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No fungicide or bactericide treatment required. Maintain mulch rings around tree bases."
        }
    },

    # ------------------ GRAPE (4) ------------------
    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "crop": "Grape",
        "pathogen_type": "Fungal",
        "causal_agent": "Guignardia bidwellii (anamorph Phyllosticta ampelicida)",
        "severity_level": "High",
        "symptoms": [
            "Small circular reddish-brown leaf spots with dark margins and tiny black pycnidia",
            "Infected berries turn light brown, soften, then shrivel into hard, black, wrinkled mummies",
            "Mummified berries remain attached to clusters",
            "Can destroy up to 80-100% of the fruit crop if left unchecked in warm, wet climates"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 24.0, "temp_optimal_max": 29.0, "temp_max": 32.0,
            "humidity_threshold": 80.0, "leaf_wetness_hours_threshold": 7.0,
            "rainfall_risk": "High (spring rains liberate ascospores)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Prune out mummified berry clusters and infected canes during dormant pruning",
                "Canopy management: shoot positioning and leaf removal around fruit zones",
                "Ensure weed-free strip beneath trellises to speed ground drying"
            ],
            "organic_controls": [
                {"name": "Copper Octanoate / Bordeaux Mixture 1%", "dosage": "10 g per Liter water", "frequency": "Early season protectant", "phi_days": 7}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Bud break until bloom", "phi_days": 14},
                {"name": "Myclobutanil 10% WP", "dosage": "1.0 g per Liter water", "frequency": "Immediate pre-bloom through 4 weeks post-bloom", "phi_days": 14}
            ],
            "cultural_practices": "Critical spray window is from early bloom through 4 weeks after bloom."
        }
    },
    "Grape___Esca_(Black_Measles)": {
        "common_name": "Grape Esca (Black Measles / Trunk Disease)",
        "crop": "Grape",
        "pathogen_type": "Fungal",
        "causal_agent": "Phaeomoniella chlamydospora / Phaeoacremonium minimum fungal complex",
        "severity_level": "Critical",
        "symptoms": [
            "Tiger-stripe pattern of interveinal chlorosis and necrosis on mature leaves",
            "Small dark-purple to black spots ('measles') scattered across berry skins",
            "Berries crack, shrivel, and develop unpalatable off-flavors",
            "Cross-section of woody trunk reveals dark necrosis and spongy white heart rot"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 25.0, "temp_optimal_max": 32.0, "temp_max": 38.0,
            "humidity_threshold": 60.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "High during winter pruning", "soil_moisture_risk": "Fluctuating / water stress"
        },
        "management": {
            "preventive_intervention": [
                "Delay winter pruning as late as possible (late winter) when wound healing is rapid",
                "Seal large pruning wounds immediately with wound protectant paint containing fungicide",
                "Avoid pruning during rainy or high-humidity days when fungal spores disperse"
            ],
            "organic_controls": [
                {"name": "Trichoderma atroviride Wound Protectant", "dosage": "Paint or spray onto fresh pruning wounds", "frequency": "Immediately after pruning", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Pruning Wound Sealant with Tebuconazole", "dosage": "Direct paint on fresh cuts >2 cm", "frequency": "Within 24 hours of cutting", "phi_days": 28}
            ],
            "cultural_practices": "No curative fungicide spray exists for systemic vascular trunk disease. Practice clean double-pruning and rogue dead vines."
        }
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "common_name": "Grape Leaf Blight (Isariopsis Spot)",
        "crop": "Grape",
        "pathogen_type": "Fungal",
        "causal_agent": "Pseudocercospora cladosporioides (syn. Phaeoisariopsis vitis)",
        "severity_level": "Moderate",
        "symptoms": [
            "Large irregular dull-brown to reddish lesions on leaf surfaces",
            "Lesions have dark borders and can coalesce to cause extensive leaf scorch",
            "Dark grayish-brown powdery spore tufts on lesion undersides",
            "Premature defoliation late in the season reduces carbohydrate reserves"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 23.0, "temp_optimal_max": 28.0, "temp_max": 33.0,
            "humidity_threshold": 80.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Prune dead canes and destroy fallen leaves after autumn leaf fall",
                "Improve canopy airflow through summer shoot trimming and suckering",
                "Maintain weed-free vine under-rows"
            ],
            "organic_controls": [
                {"name": "Bordeaux Mixture 1% (Copper + Lime)", "dosage": "10 g per Liter water", "frequency": "Post-bloom spray", "phi_days": 7}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Every 10-14 days", "phi_days": 14},
                {"name": "Carbendazim 50% WP", "dosage": "1.0 g per Liter water", "frequency": "At onset of post-monsoon spotting", "phi_days": 14}
            ],
            "cultural_practices": "Ensure balanced potassium nutrition to enhance natural cuticle resistance."
        }
    },
    "Grape___healthy": {
        "common_name": "Healthy Grape",
        "crop": "Grape",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Vigorous green palmate foliage with clean margins and no spots",
            "Strong cane growth with intact tendrils and healthy flower panicles",
            "Uniform fruit cluster development free from powdery or black rot mummies"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 22.0, "temp_optimal_max": 28.0, "temp_max": 34.0,
            "humidity_threshold": 60.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Well-drained"
        },
        "management": {
            "preventive_intervention": [
                "Perform regular canopy management and shoot tucking into trellis wires",
                "Monitor for grape berry moth and leafhopper populations",
                "Ensure controlled deficit irrigation during veraison for quality fruit"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No chemical fungicide treatment needed. Maintain clean floor management."
        }
    },

    # ------------------ BELL PEPPER (2) ------------------
    "Pepper,_bell___Bacterial_spot": {
        "common_name": "Bell Pepper Bacterial Spot",
        "crop": "Bell Pepper",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas campestris pv. vesicatoria",
        "severity_level": "High",
        "symptoms": [
            "Small, water-soaked, circular or irregular spots on leaves that turn brown",
            "Lesions often have a cracked center and faint yellow halo",
            "Leaves turn yellow and drop prematurely, causing sunscald on fruits",
            "Fruits develop small, raised, warty, blister-like spots"
        ],
        "bioclimatic_triggers": {
            "temp_min": 22.0, "temp_optimal_min": 26.0, "temp_optimal_max": 32.0, "temp_max": 36.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 5.0,
            "rainfall_risk": "High (warm driving rain)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Use certified disease-free pepper seeds or hot-water-treated seeds (50°C for 25 min)",
                "Avoid overhead sprinkler irrigation; use surface drip",
                "Disinfect transplant trays, knives, and greenhouse benches"
            ],
            "organic_controls": [
                {"name": "Copper Hydroxide 50% WP", "dosage": "2.0 g per Liter water", "frequency": "Every 7 days during warm, rainy periods", "phi_days": 1},
                {"name": "Bacillus subtilis Bio-bactericide", "dosage": "5 g per Liter water", "frequency": "Weekly preventive spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Copper Oxychloride 50% + Streptocycline (100 ppm)", "dosage": "2.5 g Copper + 0.1 g Streptocycline per L", "frequency": "Apply at first sign of spotting", "phi_days": 3}
            ],
            "cultural_practices": "Bacterial spot cannot be controlled with synthetic fungicides. Never cultivate when pepper foliage is wet."
        }
    },
    "Pepper,_bell___healthy": {
        "common_name": "Healthy Bell Pepper",
        "crop": "Bell Pepper",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Glossy, dark-green intact leaves with smooth margins",
            "Strong branching stems with healthy white blossoms",
            "Blocky, firm green or colored fruits free from lesions or sunscald"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 22.0, "temp_optimal_max": 28.0, "temp_max": 32.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Optimal", "soil_moisture_risk": "Even moisture"
        },
        "management": {
            "preventive_intervention": [
                "Maintain uniform soil moisture to prevent blossom end rot",
                "Apply balanced organic mulch to moderate root zone temperatures",
                "Scout weekly for aphids, thrips, and broad mites"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No chemical application required. Maintain good crop sanitation."
        }
    },

    # ------------------ RICE / PADDY (3) ------------------
    "Rice___Bacterial_leaf_blight": {
        "common_name": "Rice Bacterial Leaf Blight (BLB)",
        "crop": "Rice / Paddy",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas oryzae pv. oryzae",
        "severity_level": "Critical",
        "symptoms": [
            "Water-soaked stripes starting from leaf tips and margins, expanding downwards",
            "Lesions turn wavy-edged yellow-to-whitish straw color and dry up",
            "Milky bacterial ooze drops visible on young lesions in early morning dew",
            "Kresek phase (systemic seedling wilt) causing complete hill death"
        ],
        "bioclimatic_triggers": {
            "temp_min": 24.0, "temp_optimal_min": 28.0, "temp_optimal_max": 34.0, "temp_max": 38.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "Very High (cyclonic winds, heavy rains)", "soil_moisture_risk": "Flooded / saturated"
        },
        "management": {
            "preventive_intervention": [
                "Plant BLB-resistant varieties (e.g. carrying Xa21 or xa13 resistance genes)",
                "Avoid excessive nitrogen fertilization; split N applications evenly",
                "Drain flooded field temporarily for 3-5 days to arrest bacterial multiplication"
            ],
            "organic_controls": [
                {"name": "Pseudomonas fluorescens Bio-control", "dosage": "10 g per Liter water", "frequency": "Seed treatment + foliar spray at tillering", "phi_days": 0},
                {"name": "Neem Cake Soil Application", "dosage": "150 kg per Hectare", "frequency": "Basal application at transplanting", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Copper Oxychloride 50% WP + Streptocycline", "dosage": "2.5 g Copper + 0.15 g Streptocycline per L", "frequency": "Apply at initiation of disease", "phi_days": 14}
            ],
            "cultural_practices": "Do not clip rice seedling tips during transplanting as wounds are primary bacterial entry portals."
        }
    },
    "Rice___Brown_spot": {
        "common_name": "Rice Brown Spot",
        "crop": "Rice / Paddy",
        "pathogen_type": "Fungal",
        "causal_agent": "Bipolaris oryzae (syn. Helminthosporium oryzae)",
        "severity_level": "High",
        "symptoms": [
            "Small, oval to circular sesame-seed-sized brown spots on leaf blades",
            "Mature lesions develop gray or whitish centers with dark brown margins and yellow halos",
            "Grains show dark brown to black discolored spots, reducing grain quality and weight",
            "Indicator disease of nutrient-deficient, drought-stressed, or poor soil conditions"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0, "temp_optimal_min": 25.0, "temp_optimal_max": 30.0, "temp_max": 34.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Drought-stressed or deficient soils"
        },
        "management": {
            "preventive_intervention": [
                "Correct soil nutrient deficiencies (potassium, silicon, and zinc)",
                "Treat seed with hot water (53-54°C for 10-12 min) or bio-agents",
                "Maintain adequate irrigation; avoid severe soil drying during vegetative growth"
            ],
            "organic_controls": [
                {"name": "Trichoderma harzianum Seed Treatment", "dosage": "10 g per kg seed", "frequency": "Before sowing", "phi_days": 0},
                {"name": "Pseudomonas fluorescens Foliar Spray", "dosage": "5 g per Liter water", "frequency": "At active tillering and boot leaf stage", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Apply at first lesion sighting", "phi_days": 14},
                {"name": "Propiconazole 25% EC", "dosage": "1.0 ml per Liter water", "frequency": "At boot leaf stage", "phi_days": 21}
            ],
            "cultural_practices": "Apply silicon fertilizers or fly ash to strengthen rice leaf epidermis against fungal penetration."
        }
    },
    "Rice___Leaf_blast": {
        "common_name": "Rice Leaf Blast",
        "crop": "Rice / Paddy",
        "pathogen_type": "Fungal",
        "causal_agent": "Magnaporthe oryzae (syn. Pyricularia oryzae)",
        "severity_level": "Critical",
        "symptoms": [
            "Spindle-shaped or eye-shaped lesions with pointed ends on leaf blades",
            "Lesions have grayish-white centers with dark brown to reddish margins",
            "Lesions rapidly enlarge and coalesce, causing entire leaf blades to burn and dry up",
            "Can attack neck node (neck blast) causing panicles to fall over and turn completely blank"
        ],
        "bioclimatic_triggers": {
            "temp_min": 17.0, "temp_optimal_min": 22.0, "temp_optimal_max": 28.0, "temp_max": 32.0,
            "humidity_threshold": 90.0, "leaf_wetness_hours_threshold": 10.0,
            "rainfall_risk": "High (overcast days, dew, drizzling)", "soil_moisture_risk": "High humidity / saturated"
        },
        "management": {
            "preventive_intervention": [
                "Plant blast-resistant rice varieties recommended for the region",
                "Avoid heavy single doses of nitrogen; split N into 3-4 applications",
                "Maintain continuous shallow flooding (5 cm) during blast-favorable cool weather"
            ],
            "organic_controls": [
                {"name": "Pseudomonas fluorescens Talc Formulation", "dosage": "10 g per Liter water", "frequency": "Foliar spray at 15-day intervals", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Tricyclazole 75% WP (Specific Blasticide)", "dosage": "0.6 g per Liter water", "frequency": "Apply at first appearance of eye lesions", "phi_days": 21},
                {"name": "Isoprothiolane 40% EC", "dosage": "1.5 ml per Liter water", "frequency": "Apply at tillering or panicle emergence", "phi_days": 21}
            ],
            "cultural_practices": "Destroy straw and stubble from blast-infected fields; do not compost without complete heating."
        }
    },
    "Rice___Leaf_smut": {
        "common_name": "Rice Leaf Smut",
        "crop": "Rice / Paddy",
        "pathogen_type": "Fungal",
        "causal_agent": "Entyloma oryzae",
        "severity_level": "Moderate",
        "symptoms": [
            "Small, slightly raised, angular, lead-black spots (sori) on leaf blades",
            "Lesions are restricted by leaf veins, creating rectangular black linear spots",
            "Spots remain covered by leaf epidermis and release dull grayish-black mass of chlamydospores",
            "Severe infection causes premature yellowing, drying, and ragged tattered leaf tips"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0, "temp_optimal_min": 25.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Avoid excessive late-season nitrogen applications which promote lush succulent foliage",
                "Apply balanced potash (potassium) fertilizers to harden leaf tissues",
                "Ensure proper crop rotation and clean tillage to bury infected straw residue"
            ],
            "organic_controls": [
                {"name": "Pseudomonas fluorescens Bio-formulation", "dosage": "10 g per Liter water", "frequency": "Foliar spray at tillering stage", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Mancozeb 75% WP", "dosage": "2.5 g per Liter water", "frequency": "Apply at first sign of sori if disease is severe", "phi_days": 14},
                {"name": "Propiconazole 25% EC", "dosage": "1.0 ml per Liter water", "frequency": "Apply at boot stage if flag leaves are threatened", "phi_days": 21}
            ],
            "cultural_practices": "Burn or compost infected rice stubbles thoroughly; leaf smut spores overwinter on crop residue."
        }
    },
    "Rice___healthy": {
        "common_name": "Healthy Rice / Paddy",
        "crop": "Rice / Paddy",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Erect, bright-green tillers with sturdy culms and clean flag leaves",
            "Absence of spindle lesions, bacterial straw stripes, or brown specks",
            "Uniform golden panicle emergence and well-filled heavy grains"
        ],
        "bioclimatic_triggers": {
            "temp_min": 22.0, "temp_optimal_min": 26.0, "temp_optimal_max": 32.0, "temp_max": 38.0,
            "humidity_threshold": 70.0, "leaf_wetness_hours_threshold": 5.0,
            "rainfall_risk": "Adequate", "soil_moisture_risk": "Shallow submerged / saturated"
        },
        "management": {
            "preventive_intervention": [
                "Maintain alternate wetting and drying (AWD) water management to save water and aerate roots",
                "Apply balanced fertilizers based on soil health card recommendations",
                "Scout weekly for yellow stem borer egg masses and brown planthoppers"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "No fungicide or bactericide application required. Keep bunds weed-free."
        }
    },

    # ------------------ OTHER PLANTVILLAGE CLASSES (15) ------------------
    "Blueberry___healthy": {
        "common_name": "Healthy Blueberry",
        "crop": "Blueberry",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Glossy, dark-green oval leaves free from rust, scorch, or spots",
            "Healthy cane renewal and uniform berry cluster development"
        ],
        "bioclimatic_triggers": {
            "temp_min": 14.0, "temp_optimal_min": 18.0, "temp_optimal_max": 24.0, "temp_max": 28.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Acidic, moist, well-drained"
        },
        "management": {
            "preventive_intervention": [
                "Maintain acidic soil pH (4.5 - 5.5) using elemental sulfur or peat mulch",
                "Ensure pine bark mulching to retain root moisture"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No chemical application required. Prune old canes annually."
        }
    },
    "Cherry_(including_sour)___Powdery_mildew": {
        "common_name": "Cherry Powdery Mildew",
        "crop": "Cherry",
        "pathogen_type": "Fungal",
        "causal_agent": "Podosphaera clandestina",
        "severity_level": "Moderate",
        "symptoms": [
            "White circular powdery fungal patches on leaves and young shoots",
            "Leaves curl upwards, blister, and become brittle",
            "Severe infection of green cherries causes dull, deformed fruit covered in white mycelium"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 21.0, "temp_optimal_max": 27.0, "temp_max": 32.0,
            "humidity_threshold": 70.0, "leaf_wetness_hours_threshold": 2.0,
            "rainfall_risk": "Low (dry weather with high humidity favors powdery mildews)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Prune dense canopies to maximize sunlight penetration",
                "Monitor emerging leaves on shoots near the tree trunk for early mycelium"
            ],
            "organic_controls": [
                {"name": "Wettable Sulfur 80% WDG", "dosage": "3 g per Liter water", "frequency": "At petal fall and shuck fall", "phi_days": 1},
                {"name": "Potassium Bicarbonate", "dosage": "3 g per Liter water", "frequency": "Weekly curative spray", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Myclobutanil 10% WP", "dosage": "1.0 g per Liter water", "frequency": "Petal fall stage", "phi_days": 14},
                {"name": "Tebuconazole 25.9% EC", "dosage": "0.75 ml per Liter water", "frequency": "Cover spray", "phi_days": 14}
            ],
            "cultural_practices": "Sulfur sprays can burn cherry foliage if applied when temperatures exceed 30°C."
        }
    },
    "Cherry_(including_sour)___healthy": {
        "common_name": "Healthy Cherry",
        "crop": "Cherry",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Vibrant green leaves without powdery mildew, brown rot, or shot-hole lesions",
            "Plump, clean cherry fruits with bright glossy skins"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 20.0, "temp_optimal_max": 26.0, "temp_max": 30.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Well-drained"
        },
        "management": {
            "preventive_intervention": [
                "Prune in dry summer weather to reduce silver leaf fungal infection risk",
                "Maintain uniform bird netting during ripening"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No pesticide spray required. Maintain orchard sanitation."
        }
    },
    "Orange___Haunglongbing_(Citrus_greening)": {
        "common_name": "Citrus Greening (Huanglongbing / HLB)",
        "crop": "Orange",
        "pathogen_type": "Bacterial",
        "causal_agent": "Candidatus Liberibacter asiaticus (vectored by Asian Citrus Psyllid, Diaphorina citri)",
        "severity_level": "Critical",
        "symptoms": [
            "Asymmetric blotchy mottle chlorosis across leaf blades (yellowing does not mirror across vein)",
            "Yellowing of individual shoots or branches ('yellow dragon')",
            "Small, lopsided, bitter-tasting fruits that fail to color (remain green at blossom end)",
            "Darkened, aborted seeds and premature fruit drop"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0, "temp_optimal_min": 25.0, "temp_optimal_max": 32.0, "temp_max": 38.0,
            "humidity_threshold": 60.0, "leaf_wetness_hours_threshold": 2.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Plant certified disease-free budwood from registered screenhouse nurseries",
                "Aggressively monitor and control the Asian Citrus Psyllid vector on young leaf flush",
                "Apply micro-nutrient foliar sprays (zinc, manganese, iron) to support tree vigor"
            ],
            "organic_controls": [
                {"name": "Horticultural Mineral Oil (1-2%)", "dosage": "15 ml per Liter water", "frequency": "Target psyllid nymphs on new flush", "phi_days": 0},
                {"name": "Neem Seed Kernel Extract 5%", "dosage": "50 ml per Liter water", "frequency": "Every 10 days during flush", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Imidacloprid 17.8% SL (Vector suppression)", "dosage": "0.5 ml per Liter water", "frequency": "At new shoot flush", "phi_days": 15},
                {"name": "Thiamethoxam 25% WG", "dosage": "0.3 g per Liter water", "frequency": "Rotational psyllid control", "phi_days": 15}
            ],
            "cultural_practices": "NO CHEMICAL CURE EXISTS for systemic Candidatus Liberibacter bacteria. Fungicides are completely useless. Remove and burn confirmed positive trees to protect surrounding orchard."
        }
    },
    "Peach___Bacterial_spot": {
        "common_name": "Peach Bacterial Spot",
        "crop": "Peach",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas arboricola pv. pruni",
        "severity_level": "High",
        "symptoms": [
            "Small (1-3 mm) angular, water-soaked purple-black spots on leaves",
            "Lesion centers dry and fall out, giving a pronounced shot-hole or tattered appearance",
            "Severe yellowing of leaf tips and premature defoliation",
            "Pitted, cracked, gumming sunken spots on peach fruit skins"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 5.0,
            "rainfall_risk": "High (wind-driven rain, sandy soils)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Select bacterial-spot-resistant peach varieties (e.g. Candor, Clayton, Reliance)",
                "Avoid planting in blowing sandy soil sites or establish windbreaks",
                "Avoid excessive spring nitrogen which produces tender susceptible tissue"
            ],
            "organic_controls": [
                {"name": "Copper Hydroxide 50% WP (Dormant spray)", "dosage": "3 g per Liter water", "frequency": "At leaf fall and late dormant bud swell", "phi_days": 14}
            ],
            "chemical_controls": [
                {"name": "Oxytetracycline / Streptomycin", "dosage": "0.5 g per Liter water", "frequency": "Petal fall to shuck split (check local approvals)", "phi_days": 21}
            ],
            "cultural_practices": "Synthetic fungicides have no efficacy against bacterial spot. Never apply copper after petal fall as peach foliage is highly phytotoxic to copper."
        }
    },
    "Peach___healthy": {
        "common_name": "Healthy Peach",
        "crop": "Peach",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Long, lanceolate bright-green leaves free from shot-holes or leaf curl blisters",
            "Clean vigorous shoots without cankers or bacterial gumming",
            "Velvety, unblemished fruit set"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 22.0, "temp_optimal_max": 28.0, "temp_max": 32.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Well-drained sandy loam"
        },
        "management": {
            "preventive_intervention": [
                "Maintain open-center vase pruning structure for aeration and light",
                "Thin fruitlets to 15-20 cm apart along branches for optimal size",
                "Monitor for oriental fruit moth and peachtree borer"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No spray required. Maintain orchard sanitation."
        }
    },
    "Raspberry___healthy": {
        "common_name": "Healthy Raspberry",
        "crop": "Raspberry",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Vibrant green compound leaves with whitish undersides and healthy serrations",
            "Sturdy primocanes and floricanes free from cane blight or spur blight lesions"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 18.0, "temp_optimal_max": 24.0, "temp_max": 28.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Moist, rich, well-drained"
        },
        "management": {
            "preventive_intervention": [
                "Prune out spent floricanes immediately after fruiting",
                "Keep cane rows narrow (30-45 cm) for rapid morning drying"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No pesticide spray required. Maintain organic mulch."
        }
    },
    "Soybean___healthy": {
        "common_name": "Healthy Soybean",
        "crop": "Soybean",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Trifoliate leaves with vibrant, uniform green coloration",
            "No rust pustules, frog-eye leaf spots, or mosaic mottling",
            "Sturdy branching with abundant flower and pod clusters"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 4.0,
            "rainfall_risk": "Adequate", "soil_moisture_risk": "Even moisture"
        },
        "management": {
            "preventive_intervention": [
                "Inoculate seeds with Bradyrhizobium japonicum for biological nitrogen fixation",
                "Scout weekly during R1 to R3 pod development for soybean rust or pod borers"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No fungicide or bactericide treatment needed. Maintain weed-free canopy."
        }
    },
    "Squash___Powdery_mildew": {
        "common_name": "Squash Powdery Mildew",
        "crop": "Squash",
        "pathogen_type": "Fungal",
        "causal_agent": "Podosphaera xanthii (syn. Sphaerotheca fuliginea)",
        "severity_level": "High",
        "symptoms": [
            "Talcum-powder-like white fungal patches on both upper and lower leaf surfaces",
            "Patches expand to cover entire leaves and petioles",
            "Severely affected leaves turn yellow, brown, and dry out completely (paper-like)",
            "Premature defoliation leads to sunscald on fruits and reduced sugar content"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0, "temp_optimal_min": 24.0, "temp_optimal_max": 30.0, "temp_max": 35.0,
            "humidity_threshold": 70.0, "leaf_wetness_hours_threshold": 2.0,
            "rainfall_risk": "Low (favored by dry foliage with high ambient relative humidity)", "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Plant powdery-mildew-resistant squash and pumpkin hybrids",
                "Ensure wide spacing (1.5 - 2 meters between rows) for air movement",
                "Plant in full sunlight (shady areas strongly favor mildew development)"
            ],
            "organic_controls": [
                {"name": "Potassium Bicarbonate Fungicide", "dosage": "3 g per Liter water", "frequency": "Every 7 days at first white colony", "phi_days": 0},
                {"name": "Neem Oil 10,000 PPM", "dosage": "5 ml per Liter water", "frequency": "Every 7 days", "phi_days": 0},
                {"name": "Wettable Sulfur 80% WDG", "dosage": "2.5 g per Liter water", "frequency": "Every 7-10 days (avoid high heat >32°C)", "phi_days": 1}
            ],
            "chemical_controls": [
                {"name": "Azoxystrobin 23% SC", "dosage": "1.0 ml per Liter water", "frequency": "Every 10-14 days", "phi_days": 1},
                {"name": "Myclobutanil 10% WP", "dosage": "1.0 g per Liter water", "frequency": "Rotate with contact fungicides", "phi_days": 3}
            ],
            "cultural_practices": "Ensure thorough spray coverage on leaf undersides where powdery mildew colonies initiate."
        }
    },
    "Strawberry___Leaf_scorch": {
        "common_name": "Strawberry Leaf Scorch",
        "crop": "Strawberry",
        "pathogen_type": "Fungal",
        "causal_agent": "Diplocarpon earlianum",
        "severity_level": "Moderate",
        "symptoms": [
            "Irregular purplish to dark-brown spots (1-5 mm) scattered across leaf surfaces",
            "Unlike leaf spot, centers of scorch lesions remain dark purple or brown (do NOT turn white)",
            "Lesions coalesce, causing leaf margins to curl upward and look burnt (scorched)",
            "Sepals (caps) develop purple spots and dry out, degrading fruit marketability"
        ],
        "bioclimatic_triggers": {
            "temp_min": 16.0, "temp_optimal_min": 20.0, "temp_optimal_max": 26.0, "temp_max": 30.0,
            "humidity_threshold": 85.0, "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "High (frequent rain or overhead watering)", "soil_moisture_risk": "Moderate to High"
        },
        "management": {
            "preventive_intervention": [
                "Plant resistant cultivars (e.g. Allstar, Earliglow, Tribute)",
                "Avoid overhead irrigation; use drip tape beneath plastic mulch",
                "Mow or renovate strawberry beds immediately after harvest to destroy infected foliage"
            ],
            "organic_controls": [
                {"name": "Copper Soap (Copper Octanoate)", "dosage": "2 g per Liter water", "frequency": "Early spring and post-harvest", "phi_days": 1},
                {"name": "Bacillus subtilis Bio-fungicide", "dosage": "5 g per Liter water", "frequency": "Every 7 days preventively", "phi_days": 0}
            ],
            "chemical_controls": [
                {"name": "Captan 50% WP", "dosage": "2.5 g per Liter water", "frequency": "From new spring growth to bloom", "phi_days": 2},
                {"name": "Thiophanate-methyl 70% WP", "dosage": "1.0 g per Liter water", "frequency": "Pre-bloom and post-harvest", "phi_days": 3}
            ],
            "cultural_practices": "Maintain narrow matted rows (30-45 cm width) and weed regularly to promote rapid leaf drying."
        }
    },
    "Strawberry___healthy": {
        "common_name": "Healthy Strawberry",
        "crop": "Strawberry",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Lush, glossy trifoliate leaves with vibrant green coloration",
            "Sturdy crowns free from red stele or anthracnose rot",
            "Uniform white blossoms with bright yellow centers and well-formed red berries"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0, "temp_optimal_min": 18.0, "temp_optimal_max": 24.0, "temp_max": 28.0,
            "humidity_threshold": 65.0, "leaf_wetness_hours_threshold": 3.0,
            "rainfall_risk": "Moderate", "soil_moisture_risk": "Even moisture, straw mulched"
        },
        "management": {
            "preventive_intervention": [
                "Maintain clean straw or plastic mulch beneath fruiting trusses",
                "Ensure drip irrigation to prevent water on ripening berries",
                "Scout weekly for two-spotted spider mites and tarnished plant bugs"
            ],
            "organic_controls": [], "chemical_controls": [],
            "cultural_practices": "No fungicide spray required. Maintain bed weed sanitation."
        }
    }
}

# General fallback profile for unknown, ambiguous, or unmapped classes
DEFAULT_DISEASE_PROFILE = {
    "common_name": "Unverified Foliar Condition",
    "crop": "Unspecified Crop",
    "pathogen_type": "Uncertain / Unverified",
    "causal_agent": "Field Pathogen Under Review",
    "severity_level": "Under Review",
    "symptoms": [
        "Atypical leaf discoloration, chlorosis, or necrotic spotting",
        "Visual symptoms do not match a verified single pathogen profile with high certainty"
    ],
    "bioclimatic_triggers": {
        "temp_min": 16.0, "temp_optimal_min": 20.0, "temp_optimal_max": 28.0, "temp_max": 35.0,
        "humidity_threshold": 75.0, "leaf_wetness_hours_threshold": 6.0,
        "rainfall_risk": "Moderate", "soil_moisture_risk": "Moderate"
    },
    "management": {
        "preventive_intervention": [
            "Isolate the affected plant and avoid touching healthy foliage with wet hands",
            "Take a clear close-up photograph of one leaf in bright daylight for agronomic review",
            "Consult a local Krishi Vigyan Kendra (KVK) or agricultural extension specialist for confirmation"
        ],
        "organic_controls": [],
        "chemical_controls": [],
        "cultural_practices": "Do not apply chemical pesticides or fungicides without positive laboratory or agronomist confirmation."
    }
}


def get_disease_profile(disease_key: str) -> dict:
    """Retrieve detailed disease profile with deep copy to protect default state."""
    if not disease_key:
        return copy.deepcopy(DEFAULT_DISEASE_PROFILE)

    # 1. Direct hit in verified 41-class database
    if disease_key in DISEASE_PROFILES:
        return copy.deepcopy(DISEASE_PROFILES[disease_key])

    # 2. Check if disease_key can be parsed gracefully
    parts = disease_key.split("___") if "___" in disease_key else disease_key.split("_")
    crop = parts[0].replace("_", " ").strip() if parts else "Crop"
    disease_raw = parts[1].replace("_", " ").strip() if len(parts) > 1 else "Condition"

    profile = copy.deepcopy(DEFAULT_DISEASE_PROFILE)
    profile["common_name"] = f"{crop} {disease_raw}"
    profile["crop"] = crop

    if "healthy" in disease_key.lower():
        profile["severity_level"] = "Healthy"
        profile["pathogen_type"] = "None"
        profile["causal_agent"] = "Healthy Plant"
        profile["symptoms"] = ["Normal foliage coloration without identifiable disease symptoms."]
        profile["management"]["organic_controls"] = []
        profile["management"]["chemical_controls"] = []
        profile["management"]["preventive_intervention"] = [
            "Continue standard crop care and routine scouting.",
            "Maintain balanced watering and crop nutrition."
        ]
        profile["management"]["cultural_practices"] = "No chemical intervention needed."

    return profile
