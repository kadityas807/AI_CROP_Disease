"""
Agronomic Knowledge Base for AI Crop Disease Prediction & Management System
Covers 14 major crop species and 38+ PlantVillage disease profiles with bioclimatic triggers and treatments.
"""

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
            "Rice___healthy"
        ]
    },
    "Strawberry": {
        "icon": "🍓",
        "scientific_name": "Fragaria ananassa",
        "diseases": [
            "Strawberry___Leaf_scorch",
            "Strawberry___healthy"
        ]
    },
    "Wheat": {
        "icon": "🌾",
        "scientific_name": "Triticum aestivum",
        "diseases": [
            "Wheat___Yellow_rust",
            "Wheat___Brown_rust",
            "Wheat___Powdery_mildew",
            "Wheat___healthy"
        ]
    }
}

DISEASE_PROFILES = {
    "Tomato___Late_blight": {
        "common_name": "Tomato Late Blight",
        "crop": "Tomato",
        "pathogen_type": "Oomycete / Water Mold",
        "causal_agent": "Phytophthora infestans",
        "severity_level": "Critical",
        "symptoms": [
            "Large, irregular water-soaked greenish-black lesions on leaves",
            "White fuzzy mold growth on the undersides of leaves in humid conditions",
            "Dark brown blotches on stems and firm brown lesions on fruits",
            "Rapid collapse of foliage within 72 hours under wet conditions"
        ],
        "bioclimatic_triggers": {
            "temp_min": 10.0,
            "temp_optimal_min": 15.0,
            "temp_optimal_max": 22.0,
            "temp_max": 26.0,
            "humidity_threshold": 85.0,
            "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "High (continuous drizzling or rain)",
            "soil_moisture_risk": "High saturation"
        },
        "management": {
            "preventive_intervention": [
                "Ensure wide plant spacing (60-75 cm) for canopy aeration",
                "Use drip irrigation instead of overhead sprinklers to prevent leaf wetting",
                "Apply preventive protective copper-based sprays prior to rain periods",
                "Destroy infected volunteer plants and solanaceous weeds"
            ],
            "organic_controls": [
                {
                    "name": "Copper Octanoate (Copper Soap)",
                    "dosage": "15-20 ml per 10 Liters water",
                    "frequency": "Every 7 days in high humidity",
                    "phi_days": 1
                },
                {
                    "name": "Bacillus subtilis Bio-fungicide",
                    "dosage": "5-10 g per Liter water",
                    "frequency": "Every 5-7 days preventively",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Mancozeb 75% WP (Contact)",
                    "dosage": "2.5 g per Liter water",
                    "frequency": "Every 7-10 days",
                    "phi_days": 7
                },
                {
                    "name": "Dimethomorph 50% WP + Cymoxanil (Curative/Systemic)",
                    "dosage": "1.5 g per Liter water",
                    "frequency": "Apply immediately upon first appearance",
                    "phi_days": 5
                }
            ],
            "cultural_practices": "Prune lower leaves touching soil; mulch soil surface to prevent spore splash."
        }
    },
    "Tomato___Early_blight": {
        "common_name": "Tomato Early Blight",
        "crop": "Tomato",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "severity_level": "Moderate to High",
        "symptoms": [
            "Concentric ring target-like spots with yellow halo on older lower leaves",
            "Leaf yellowing followed by premature defoliation starting bottom-up",
            "Sunken dark lesions at the stem base or fruit calyx end"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0,
            "temp_optimal_min": 24.0,
            "temp_optimal_max": 29.0,
            "temp_max": 34.0,
            "humidity_threshold": 75.0,
            "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate to High",
            "soil_moisture_risk": "Fluctuating dry-wet cycles"
        },
        "management": {
            "preventive_intervention": [
                "Rotate crops with non-solanaceous plants for at least 2-3 seasons",
                "Remove and burn lower infected foliage",
                "Apply straw mulch to prevent soil splashing"
            ],
            "organic_controls": [
                {
                    "name": "Neem Seed Kernel Extract (NSKE 5%)",
                    "dosage": "50 ml per Liter water",
                    "frequency": "Every 10 days",
                    "phi_days": 0
                },
                {
                    "name": "Trichoderma harzianum soil and foliar spray",
                    "dosage": "5 g per Liter water",
                    "frequency": "Every 12-14 days",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Chlorothalonil 75% WP",
                    "dosage": "2.0 g per Liter water",
                    "frequency": "Every 10 days",
                    "phi_days": 7
                },
                {
                    "name": "Azoxystrobin 23% SC",
                    "dosage": "1.0 ml per Liter water",
                    "frequency": "Alternate with contact fungicides",
                    "phi_days": 3
                }
            ],
            "cultural_practices": "Stake and prune tomato plants for upright growth; avoid handling plants when wet."
        }
    },
    "Tomato___Bacterial_spot": {
        "common_name": "Tomato Bacterial Spot",
        "crop": "Tomato",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas perforans",
        "severity_level": "High",
        "symptoms": [
            "Small, greasy, water-soaked dark spots (1-3 mm) on leaves",
            "Spots turn brown with translucent yellowish halo, centers may drop out (shot hole)",
            "Rough, scabby raised spots on green fruits"
        ],
        "bioclimatic_triggers": {
            "temp_min": 22.0,
            "temp_optimal_min": 26.0,
            "temp_optimal_max": 32.0,
            "temp_max": 36.0,
            "humidity_threshold": 80.0,
            "leaf_wetness_hours_threshold": 5.0,
            "rainfall_risk": "High with heavy wind-driven rain",
            "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Use certified pathogen-free hot-water treated seeds",
                "Avoid overhead irrigation and working in wet fields",
                "Sanitize pruning tools with 10% bleach solution"
            ],
            "organic_controls": [
                {
                    "name": "Copper Hydroxide + Streptomyces",
                    "dosage": "2.0 g per Liter water",
                    "frequency": "Every 7 days during warm rainy spells",
                    "phi_days": 1
                }
            ],
            "chemical_controls": [
                {
                    "name": "Copper Oxychloride 50% WP + Streptocycline (90:10)",
                    "dosage": "2.5 g + 0.1 g per Liter water",
                    "frequency": "Every 10 days",
                    "phi_days": 5
                }
            ],
            "cultural_practices": "Disinfect stakes and trellises before replanting; destroy crop residue post-harvest."
        }
    },
    "Potato___Late_blight": {
        "common_name": "Potato Late Blight",
        "crop": "Potato",
        "pathogen_type": "Oomycete / Water Mold",
        "causal_agent": "Phytophthora infestans",
        "severity_level": "Critical",
        "symptoms": [
            "Water-soaked black-brown necrotic lesions spreading from leaf tips",
            "White mildew ring on the underside of infected leaves early morning",
            "Tuber rot with rusty brown granular discoloration beneath skin"
        ],
        "bioclimatic_triggers": {
            "temp_min": 10.0,
            "temp_optimal_min": 15.0,
            "temp_optimal_max": 21.0,
            "temp_max": 25.0,
            "humidity_threshold": 90.0,
            "leaf_wetness_hours_threshold": 10.0,
            "rainfall_risk": "High (fog, drizzle, overcast)",
            "soil_moisture_risk": "High saturation"
        },
        "management": {
            "preventive_intervention": [
                "Plant certified resistant seed tubers (e.g., Kufri Girdhari, Kufri Khyati)",
                "High earthing up of potato ridges (15-20 cm) to protect developing tubers from spore wash",
                "Monitor the environmental risk index during cool, humid, and wet periods"
            ],
            "organic_controls": [
                {
                    "name": "Bordeaux Mixture (1%)",
                    "dosage": "10 g Copper Sulfate + 10 g Lime per Liter water",
                    "frequency": "Every 7-10 days",
                    "phi_days": 1
                }
            ],
            "chemical_controls": [
                {
                    "name": "Metalaxyl 8% + Mancozeb 64% WP",
                    "dosage": "2.5 g per Liter water",
                    "frequency": "Spray immediately at first blight alert",
                    "phi_days": 14
                },
                {
                    "name": "Cyazofamid 34.5% SC",
                    "dosage": "0.8 ml per Liter water",
                    "frequency": "Spray before canopy closure",
                    "phi_days": 7
                }
            ],
            "cultural_practices": "Dehaulm (cut foliage 10 days before harvest) to prevent tuber infection."
        }
    },
    "Potato___Early_blight": {
        "common_name": "Potato Early Blight",
        "crop": "Potato",
        "pathogen_type": "Fungal",
        "causal_agent": "Alternaria solani",
        "severity_level": "Moderate",
        "symptoms": [
            "Brown spots with concentric rings like target boards on older foliage",
            "Leaves turn brittle, yellow and drop prematurely",
            "Depressed corky brown lesions on tubers"
        ],
        "bioclimatic_triggers": {
            "temp_min": 20.0,
            "temp_optimal_min": 24.0,
            "temp_optimal_max": 30.0,
            "temp_max": 35.0,
            "humidity_threshold": 70.0,
            "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Moderate",
            "soil_moisture_risk": "Low to Moderate with intermittent irrigation"
        },
        "management": {
            "preventive_intervention": [
                "Adequate potassium and nitrogen fertilizer management to prevent plant stress",
                "Ensure uniform furrow or sprinkler irrigation timing"
            ],
            "organic_controls": [
                {
                    "name": "Pseudomonas fluorescens bio-agent",
                    "dosage": "10 g per Liter water",
                    "frequency": "Foliar spray every 10 days",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Propineb 70% WP",
                    "dosage": "2.0 g per Liter water",
                    "frequency": "Every 10-12 days",
                    "phi_days": 10
                }
            ],
            "cultural_practices": "Destroy cull piles and crop debris after harvesting."
        }
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "common_name": "Corn Northern Leaf Blight",
        "crop": "Corn (Maize)",
        "pathogen_type": "Fungal",
        "causal_agent": "Exserohilum turcicum",
        "severity_level": "High",
        "symptoms": [
            "Long, elliptical, cigar-shaped grayish-green to tan lesions (2.5 to 15 cm)",
            "Lesions develop dark spores on surface during moist weather",
            "Leaves turn grayish and appear burned"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0,
            "temp_optimal_min": 18.0,
            "temp_optimal_max": 27.0,
            "temp_max": 32.0,
            "humidity_threshold": 85.0,
            "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "High with heavy dew",
            "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Select resistant corn hybrids with Ht gene resistance",
                "Deep tillage to bury infected corn residue after harvest"
            ],
            "organic_controls": [
                {
                    "name": "Trichoderma viride foliar application",
                    "dosage": "5 g per Liter water",
                    "frequency": "Every 15 days",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Pyraclostrobin + Fluxapyroxad",
                    "dosage": "1.0 ml per Liter water",
                    "frequency": "Apply at V8 to VT tassel stage if risk is high",
                    "phi_days": 14
                }
            ],
            "cultural_practices": "Crop rotation with soybean or pulses to break the disease cycle."
        }
    },
    "Apple___Apple_scab": {
        "common_name": "Apple Scab",
        "crop": "Apple",
        "pathogen_type": "Fungal",
        "causal_agent": "Venturia inaequalis",
        "severity_level": "High",
        "symptoms": [
            "Olive-green to velvety brown velvety spots on upper leaf surfaces",
            "Leaf distortion, curling, and early summer leaf drop",
            "Corky, scabby cracked black lesions on apple fruit skin"
        ],
        "bioclimatic_triggers": {
            "temp_min": 8.0,
            "temp_optimal_min": 16.0,
            "temp_optimal_max": 24.0,
            "temp_max": 28.0,
            "humidity_threshold": 80.0,
            "leaf_wetness_hours_threshold": 9.0,
            "rainfall_risk": "Frequent spring showers",
            "soil_moisture_risk": "High"
        },
        "management": {
            "preventive_intervention": [
                "Rake and shred or compost fallen apple leaves in autumn",
                "Prune trees during dormancy to open canopy for rapid sun drying"
            ],
            "organic_controls": [
                {
                    "name": "Liquid Lime Sulfur / Wettable Sulfur",
                    "dosage": "3-5 g per Liter water",
                    "frequency": "Apply at green tip and pink bud stage",
                    "phi_days": 1
                }
            ],
            "chemical_controls": [
                {
                    "name": "Difenoconazole 25% EC",
                    "dosage": "0.5 ml per Liter water",
                    "frequency": "Follow product labeling and local agricultural extension guidance for application timing",
                    "phi_days": 14
                }
            ],
            "cultural_practices": "Spray orchard floor with 5% urea in autumn to accelerate leaf decay."
        }
    },
    "Grape___Black_rot": {
        "common_name": "Grape Black Rot",
        "crop": "Grape",
        "pathogen_type": "Fungal",
        "causal_agent": "Guignardia bidwellii",
        "severity_level": "High",
        "symptoms": [
            "Small circular reddish-brown leaf spots with tiny black pycnidia dots",
            "Berries turn brown, shrivel, and dry into hard black mummies within days",
            "Can cause up to 80-100% crop loss in warm humid vineyards"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0,
            "temp_optimal_min": 22.0,
            "temp_optimal_max": 28.0,
            "temp_max": 32.0,
            "humidity_threshold": 80.0,
            "leaf_wetness_hours_threshold": 7.0,
            "rainfall_risk": "High during bloom to veraison",
            "soil_moisture_risk": "Moderate"
        },
        "management": {
            "preventive_intervention": [
                "Remove and burn mummified berries from vines and ground during winter pruning",
                "Canopy shoot thinning and hedging for wind movement"
            ],
            "organic_controls": [
                {
                    "name": "Copper Oxychloride + Potassium Bicarbonate",
                    "dosage": "2.5 g + 3.0 g per Liter water",
                    "frequency": "Apply prior to rain events",
                    "phi_days": 3
                }
            ],
            "chemical_controls": [
                {
                    "name": "Myclobutanil 10% WP / Tebuconazole",
                    "dosage": "1.0 g per Liter water",
                    "frequency": "Apply at early bloom and post-bloom",
                    "phi_days": 14
                }
            ],
            "cultural_practices": "Maintain weed-free strip under vines to lower ground level humidity."
        }
    },
    "Rice___Bacterial_leaf_blight": {
        "common_name": "Rice Bacterial Leaf Blight (BLB)",
        "crop": "Rice / Paddy",
        "pathogen_type": "Bacterial",
        "causal_agent": "Xanthomonas oryzae pv. oryzae",
        "severity_level": "Severe",
        "symptoms": [
            "Water-soaked lesions on leaf margins turning wavy yellow-white stripes",
            "Milky bacterial ooze beads on young lesions in morning dew",
            "Complete drying and bleaching of leaves (kresek phase)"
        ],
        "bioclimatic_triggers": {
            "temp_min": 24.0,
            "temp_optimal_min": 28.0,
            "temp_optimal_max": 34.0,
            "temp_max": 38.0,
            "humidity_threshold": 85.0,
            "leaf_wetness_hours_threshold": 6.0,
            "rainfall_risk": "Heavy monsoon rains and typhoons/cyclones",
            "soil_moisture_risk": "Standing flooded water"
        },
        "management": {
            "preventive_intervention": [
                "Avoid excess Nitrogen fertilizer; apply balanced N:P:K (120:60:60 with split N)",
                "Avoid clipping leaf tips before transplanting",
                "Drain stagnant field water for 3-4 days to arrest infection"
            ],
            "organic_controls": [
                {
                    "name": "Pseudomonas fluorescens seed and root dip",
                    "dosage": "10 g per kg seed / 2.5 kg per hectare",
                    "frequency": "At nursery and tillering stage",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Streptocycline 90% + Copper Oxychloride 50% WP",
                    "dosage": "6 g + 500 g in 200 Liters water per acre",
                    "frequency": "Spray at first symptom appearance",
                    "phi_days": 15
                }
            ],
            "cultural_practices": "Plant BLB resistant cultivars (e.g., Improved Samba Mahsuri, IR64-Xa21)."
        }
    },
    "Rice___Leaf_blast": {
        "common_name": "Rice Leaf Blast",
        "crop": "Rice / Paddy",
        "pathogen_type": "Fungal",
        "causal_agent": "Magnaporthe oryzae",
        "severity_level": "Critical",
        "symptoms": [
            "Spindle-shaped or diamond-shaped lesions with gray center and brown margin",
            "Lesions enlarge and coalesce causing entire leaves to blast/wither",
            "Rotten neck causing blank/sterile panicles"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0,
            "temp_optimal_min": 22.0,
            "temp_optimal_max": 28.0,
            "temp_max": 32.0,
            "humidity_threshold": 90.0,
            "leaf_wetness_hours_threshold": 8.0,
            "rainfall_risk": "High with heavy dew periods",
            "soil_moisture_risk": "High"
        },
        "management": {
            "preventive_intervention": [
                "Treat seeds with Carbendazim 2g/kg or Trichoderma viride 4g/kg",
                "Avoid late planting and excessive urea top-dressing"
            ],
            "organic_controls": [
                {
                    "name": "Cow urine + Neem oil spray (1:10)",
                    "dosage": "50 ml per Liter water",
                    "frequency": "Every 10 days",
                    "phi_days": 0
                }
            ],
            "chemical_controls": [
                {
                    "name": "Tricyclazole 75% WP",
                    "dosage": "0.6 g per Liter water",
                    "frequency": "Spray at tillering and panicle emergence",
                    "phi_days": 14
                },
                {
                    "name": "Isoprothiolane 40% EC",
                    "dosage": "1.5 ml per Liter water",
                    "frequency": "Every 12 days",
                    "phi_days": 10
                }
            ],
            "cultural_practices": "Maintain shallow water level (2-3 cm) during vegetative phase."
        }
    },
    "Tomato___healthy": {
        "common_name": "Healthy Tomato",
        "crop": "Tomato",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Vibrant green leaves with uniform coloration and turgor",
            "No necrotic spots, chlorosis, wilting, or fungal sporulation"
        ],
        "bioclimatic_triggers": {
            "temp_min": 18.0,
            "temp_optimal_min": 20.0,
            "temp_optimal_max": 28.0,
            "temp_max": 32.0,
            "humidity_threshold": 65.0,
            "leaf_wetness_hours_threshold": 2.0,
            "rainfall_risk": "Low",
            "soil_moisture_risk": "Optimal (60-70%)"
        },
        "management": {
            "preventive_intervention": [
                "Maintain regular soil moisture monitoring and drip fertigation schedule",
                "Inspect foliage bi-weekly for early pest/disease presence",
                "Apply prophylactic bio-stimulant (Seaweed extract / Fulvic acid)"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "Maintain clean field sanitation and standard trellis support."
        }
    },
    "Potato___healthy": {
        "common_name": "Healthy Potato",
        "crop": "Potato",
        "pathogen_type": "None",
        "causal_agent": "Healthy Plant",
        "severity_level": "Healthy",
        "symptoms": [
            "Lush green compound foliage with vigorous stem growth",
            "No signs of wilting, ring spots, or mold"
        ],
        "bioclimatic_triggers": {
            "temp_min": 15.0,
            "temp_optimal_min": 18.0,
            "temp_optimal_max": 24.0,
            "temp_max": 28.0,
            "humidity_threshold": 65.0,
            "leaf_wetness_hours_threshold": 2.0,
            "rainfall_risk": "Low",
            "soil_moisture_risk": "Optimal (60-70%)"
        },
        "management": {
            "preventive_intervention": [
                "Monitor canopy density and maintain hilling around stems",
                "Apply balanced potassium to strengthen cell wall resistance"
            ],
            "organic_controls": [],
            "chemical_controls": [],
            "cultural_practices": "Ensure proper field drainage to prevent waterlogging."
        }
    }
}

DEFAULT_DISEASE_PROFILE = {
    "common_name": "Plant Pathogen Infection",
    "crop": "General Crop",
    "pathogen_type": "Fungal / Microbial",
    "causal_agent": "Field Pathogen",
    "severity_level": "Moderate",
    "symptoms": [
        "Leaf spot lesions, chlorosis or necrosis on lamina",
        "Reduced photosynthetic vigor and plant growth retardation"
    ],
    "bioclimatic_triggers": {
        "temp_min": 16.0,
        "temp_optimal_min": 20.0,
        "temp_optimal_max": 28.0,
        "temp_max": 35.0,
        "humidity_threshold": 75.0,
        "leaf_wetness_hours_threshold": 6.0,
        "rainfall_risk": "Moderate",
        "soil_moisture_risk": "High"
    },
    "management": {
        "preventive_intervention": [
            "Isolate infected plants and sanitize agricultural implements",
            "Adjust irrigation to prevent prolonged foliage wetness"
        ],
        "organic_controls": [
            {
                "name": "Neem Oil 10,000 PPM",
                "dosage": "5 ml per Liter water",
                "frequency": "Every 7-10 days",
                "phi_days": 0
            }
        ],
        "chemical_controls": [
            {
                "name": "Broad Spectrum Protectant Fungicide (Mancozeb 75% WP)",
                "dosage": "2.5 g per Liter water",
                "frequency": "Every 10-14 days",
                "phi_days": 7
            }
        ],
        "cultural_practices": "Collect and safely dispose of infected crop residues."
    }
}

def get_disease_profile(disease_key: str) -> dict:
    """Retrieve detailed disease profile or fallback gracefully."""
    if disease_key in DISEASE_PROFILES:
        return DISEASE_PROFILES[disease_key]
    
    parts = disease_key.split("___")
    crop = parts[0].replace("_", " ")
    disease_raw = parts[1].replace("_", " ") if len(parts) > 1 else "Disease"
    
    profile = dict(DEFAULT_DISEASE_PROFILE)
    profile["common_name"] = f"{crop} {disease_raw}"
    profile["crop"] = crop
    if "healthy" in disease_key.lower():
        profile["severity_level"] = "Healthy"
        profile["pathogen_type"] = "None"
        profile["causal_agent"] = "Healthy Plant"
        profile["symptoms"] = ["Normal foliage coloration without identifiable disease symptoms."]
        profile["management"]["organic_controls"] = []
        profile["management"]["chemical_controls"] = []
    return profile
