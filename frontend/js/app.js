const state = {
  currentFile: null,
  targetCrop: "Tomato",
  cropStage: "Vegetative",
  temperature: 23.5,
  relativeHumidity: 88,
  rainfallMm: 15,
  leafWetnessHours: 8,
  windSpeedKmh: 12,
  hasPrediction: false,
  latestPrediction: null,
  latestResultData: null,
  currentLanguage: "en",
  isSpeaking: false,
};

const TRANSLATIONS = {
  en: {
    nav_overview: "Overview",
    nav_check: "Crop Check",
    nav_guidance: "Treatment Notes",
    nav_history: "History",
    eyebrow_text: "CROP HEALTH DECISION SUPPORT",
    hero_title: "A clearer first look<br class=\"desktop-break\" /> at <span class=\"gradient-text\">crop health.</span>",
    hero_copy: "Compare a leaf-photo match with environmental favorability and local crop guidance. Use the result for review—not a confirmed diagnosis.",
    hero_btn: "Start a crop check",
    note_title: "Built for careful decisions",
    note_copy: "Model scores are not probabilities. Confirm important crop decisions with a local expert.",
    kicker_photo: "PHOTO",
    upload_title: "Upload a leaf photo",
    upload_subtitle: "Choose a clear photo of one affected leaf.",
    dropzone_main: "Drop your leaf photo here",
    dropzone_sub: "Drag and drop, paste an image, or use the browse button below",
    btn_browse: "Browse files",
    btn_camera: "Camera",
    hero_history_btn: "View previous scans",
    btn_remove: "Remove photo",
    status_no_photo: "No photo selected",
    sample_label: "Or test with a sample leaf",
    info_strip: "Photo checks use a saved MobileNetV2 model with 41 canonical classes. Field photos can differ from training images, so confirm important results with a local expert.",
    kicker_field: "FIELD DETAILS",
    field_title: "Tell us about the field",
    field_subtitle: "A bit of context helps put the photo in perspective.",
    geo_title: "Photo location and date",
    label_optional: "Optional",
    lbl_lat: "Latitude",
    lbl_lon: "Longitude",
    lbl_date: "Image capture date (UTC)",
    status_simulation_mode: "Simulation mode · enter all three details above to request aligned historical weather.",
    lbl_crop: "Crop",
    lbl_stage: "Growth stage",
    preset_label: "Or try a weather preset",
    btn_check_leaf: "Check this leaf",
    status_add_photo: "Add a photo to begin.",
    accordion_weather: "Adjust simulated weather",
    lbl_temp: "Temperature",
    lbl_humidity: "Humidity",
    lbl_wetness: "Leaf wetness",
    lbl_rain: "Rainfall today",
    lbl_wind: "Wind speed",
    kicker_results: "YOUR CROP CHECK",
    badge_waiting: "Waiting for photo",
    results_title: "Your crop check",
    results_subtitle: "A clear summary of the image match and field conditions.",
    summary_title_empty: "Your crop check will appear here",
    summary_copy_empty: "Upload a clear leaf photo and select “Check this leaf” to see what the image model found and what to inspect next.",
    lbl_combined_index: "Combined index",
    lbl_likely_match: "Most likely image match",
    lbl_waiting_res: "Your result will appear here",
    lbl_model_match: "Image-model match score",
    lbl_not_prob: "A model score, not a probability.",
    lbl_field_cond: "Field conditions",
    tag_simulated: "Simulated weather",
    copy_field_empty: "The field conditions summary will appear after your crop check.",
    lbl_symptoms: "What to look for",
    lbl_reasoning: "Why this came up",
    lbl_other_matches: "Other possible matches",
    lbl_not_val_prob: "Model scores are not validated probabilities.",
    lbl_disclaimer: "Use this as decision-support information only. For important crop decisions, ask a local agronomist or seek lab confirmation.",
    kicker_guidance: "FIELD NOTES",
    guidance_title: "What to do next",
    guidance_subtitle: "Review local guidance before applying any treatment.",
    btn_listen: "Listen to advice",
    btn_stop_listen: "Stop listening",
    guidance_empty: "Run a crop check to see relevant first steps and field guidance here.",
    tab_immediate: "First steps",
    tab_organic: "Organic",
    tab_chemical: "Chemical",
    tab_cultural: "Farm advice",
    caution_text: "Always follow local regulations and product labels. Confirm treatment choices with a qualified local agricultural advisor.",
    chat_kicker: "A HAND WHEN YOU NEED ONE",
    chat_title: "Crop Assistant",
    chat_subtitle: "Your farming companion • Local AI",
    chat_note: "Answers use this project's local crop knowledge base. No external service or API key is used.",
    chat_initial: "Hi! 🌱 Ask me about crop diseases, symptoms, or treatment guidance.",
    btn_send: "Send",
    chat_disclaimer: "Crop guidance is not a confirmed diagnosis or a substitute for local agricultural advice.",
    history_kicker: "FIELD TELEMETRY",
    history_clear: "Clear history",
    history_title: "Recent Diagnosis Scans",
    history_subtitle: "Persisted locally in SQLite for farmer records and field monitoring.",
    history_empty: "No recent scans recorded yet. Run a crop check to save results.",
  },
  hi: {
    nav_overview: "अवलोकन",
    nav_check: "फसल जांच",
    nav_guidance: "उपचार सलाह",
    nav_history: "इतिहास",
    eyebrow_text: "फसल स्वास्थ्य निर्णय सहायता",
    hero_title: "फसल स्वास्थ्य पर<br class=\"desktop-break\" /> एक <span class=\"gradient-text\">सटीक नज़र।</span>",
    hero_copy: "पत्ती की तस्वीर और मौसम के जोखिम के आधार पर विश्वसनीय कृषि सलाह प्राप्त करें। यह प्राथमिक समीक्षा के लिए है - प्रयोगशाला निदान नहीं।",
    hero_btn: "जांच शुरू करें",
    note_title: "सावधानीपूर्वक निर्णय",
    note_copy: "मॉडल स्कोर संभावना नहीं हैं। महत्वपूर्ण निर्णयों के लिए स्थानीय कृषि विशेषज्ञ से संपर्क करें।",
    kicker_photo: "फोटो",
    upload_title: "पत्ती की फोटो अपलोड करें",
    upload_subtitle: "प्रभावित पत्ती की स्पष्ट फोटो चुनें।",
    dropzone_main: "पत्ती की फोटो यहाँ डालें",
    dropzone_sub: "फोटो खींचकर डालें, पेस्ट करें या नीचे दिए बटन से चुनें",
    btn_browse: "फोटो चुनें",
    btn_camera: "कैमरा",
    hero_history_btn: "पुराने स्कैन देखें",
    btn_remove: "फोटो हटाएं",
    status_no_photo: "कोई फोटो नहीं चुनी गई",
    sample_label: "या नमूना पत्ती से परीक्षण करें",
    info_strip: "जांच 41 प्रमाणित वर्गों वाले MobileNetV2 मॉडल द्वारा की जाती है। महत्वपूर्ण परिणामों की पुष्टि स्थानीय विशेषज्ञ से करें।",
    kicker_field: "खेत विवरण",
    field_title: "खेत की स्थिति बताएं",
    field_subtitle: "खेत का वातावरण फोटो की सही समझ में मदद करता है।",
    geo_title: "फोटो का स्थान और तारीख",
    label_optional: "वैकल्पिक",
    lbl_lat: "अक्षांश (Latitude)",
    lbl_lon: "देशांतर (Longitude)",
    lbl_date: "फोटो लेने की तारीख (UTC)",
    status_simulation_mode: "सिमुलेशन मोड · वास्तविक ऐतिहासिक मौसम प्राप्त करने हेतु तीनों विवरण भरें।",
    lbl_crop: "फसल",
    lbl_stage: "वृद्धि चरण",
    preset_label: "या पूर्व-निर्धारित मौसम चुनें",
    btn_check_leaf: "पत्ती की जांच करें",
    status_add_photo: "शुरू करने के लिए एक फोटो जोड़ें।",
    accordion_weather: "सिम्युलेटेड मौसम बदलें",
    lbl_temp: "तापमान",
    lbl_humidity: "हवा में नमी (Humidity)",
    lbl_wetness: "पत्ती का गीलापन",
    lbl_rain: "आज की बारिश",
    lbl_wind: "हवा की गति",
    kicker_results: "जांच परिणाम",
    badge_waiting: "फोटो की प्रतीक्षा है",
    results_title: "आपकी फसल जांच",
    results_subtitle: "पत्ती और मौसम की स्थिति का स्पष्ट सारांश।",
    summary_title_empty: "आपका परिणाम यहाँ दिखाई देगा",
    summary_copy_empty: "एक स्पष्ट पत्ती की फोटो अपलोड करें और 'पत्ती की जांच करें' पर क्लिक करें।",
    lbl_combined_index: "समग्र जोखिम सूचकांक",
    lbl_likely_match: "संभावित रोग पहचान",
    lbl_waiting_res: "आपका परिणाम यहाँ दिखेगा",
    lbl_model_match: "मॉडल पहचान स्कोर",
    lbl_not_prob: "यह मॉडल स्कोर है, पूर्ण पुष्टि नहीं।",
    lbl_field_cond: "खेत की स्थिति",
    tag_simulated: "अनुमानित मौसम",
    copy_field_empty: "खेत की स्थिति का सारांश जांच के बाद यहाँ दिखेगा।",
    lbl_symptoms: "क्या लक्षण देखें",
    lbl_reasoning: "यह परिणाम क्यों आया",
    lbl_other_matches: "अन्य संभावित रोग",
    lbl_not_val_prob: "मॉडल स्कोर सत्यापित संभावना नहीं हैं।",
    lbl_disclaimer: "इसे केवल निर्णय-सहायता के रूप में उपयोग करें। महत्वपूर्ण निर्णयों हेतु कृषि वैज्ञानिक से परामर्श लें।",
    kicker_guidance: "कृषि नोट्स",
    guidance_title: "आगे क्या कदम उठाएं",
    guidance_subtitle: "उपचार से पहले स्थानीय दिशानिर्देशों की समीक्षा करें।",
    btn_listen: "सलाह सुनें (ऑडियो)",
    btn_stop_listen: "सुनना रोकें",
    guidance_empty: "उपचार और प्रबंधन सलाह देखने के लिए फसल जांच चलाएं।",
    tab_immediate: "शुरुआती कदम",
    tab_organic: "जैविक उपचार",
    tab_chemical: "रासायनिक नियंत्रण",
    tab_cultural: "खेत प्रबंधन",
    caution_text: "हमेशा स्थानीय नियमों और उत्पाद लेबल का पालन करें। किसी भी दवा के प्रयोग से पहले कृषि अधिकारी से सलाह लें।",
    chat_kicker: "कृषि सहायता",
    chat_title: "फसल सहायक",
    chat_subtitle: "आपका कृषि साथी • स्थानीय AI",
    chat_note: "उत्तर स्थानीय कृषि ज्ञान आधार से आते हैं। कोई बाहरी इंटरनेट या API कुंजी आवश्यक नहीं है।",
    chat_initial: "नमस्ते! 🌱 मुझसे फसल के रोगों, लक्षणों या उपचार के बारे में पूछें।",
    btn_send: "भेजें",
    chat_disclaimer: "कृषि सलाह केवल निर्णय सहायता है, विशेषज्ञ सलाह का विकल्प नहीं।",
    history_kicker: "खेत टेलीमेट्री",
    history_clear: "इतिहास साफ़ करें",
    history_title: "हाल के जांच रिकॉर्ड",
    history_subtitle: "किसान रिकॉर्ड और फील्ड निगरानी के लिए SQLite में सुरक्षित।",
    history_empty: "अभी तक कोई स्कैन रिकॉर्ड नहीं है। परिणाम सहेजने के लिए जांच चलाएं।",
  }
};

document.addEventListener("DOMContentLoaded", () => {
  initUpload();
  initControls();
  initSampleLeaves();
  initWeatherPresets();
  initPlanTabs();
  initializeWeatherMode();
  initCropChat();
  initScrollSpy();
  initClipboardPaste();
  initMobileResultFocus();
  initLanguageSwitcher();
  initAudioGuidance();
  initScanHistory();
});

function initUpload() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");

  dropzone.addEventListener("click", () => fileInput.click());
  fileInput.addEventListener("click", event => event.stopPropagation());
  document.getElementById("browse-files").addEventListener("click", event => {
    event.stopPropagation();
    fileInput.click();
  });
  dropzone.addEventListener("keydown", event => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      fileInput.click();
    }
  });
  dropzone.addEventListener("dragover", event => {
    event.preventDefault();
    dropzone.classList.add("dragover");
  });
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));
  dropzone.addEventListener("drop", event => {
    event.preventDefault();
    dropzone.classList.remove("dragover");
    if (event.dataTransfer.files[0]) selectImage(event.dataTransfer.files[0]);
  });
  fileInput.addEventListener("change", event => {
    if (event.target.files[0]) selectImage(event.target.files[0]);
  });
  const cameraBtn = document.getElementById("btn-camera");
  const cameraInput = document.getElementById("camera-input");
  if (cameraBtn && cameraInput) {
    cameraBtn.addEventListener("click", event => {
      event.stopPropagation();
      cameraInput.click();
    });
    cameraInput.addEventListener("change", event => {
      if (event.target.files && event.target.files[0]) selectImage(event.target.files[0]);
    });
  }
  document.getElementById("remove-image").addEventListener("click", event => {
    state.currentFile = null;
    fileInput.value = "";
    const camInput = document.getElementById("camera-input");
    if (camInput) camInput.value = "";
    document.getElementById("preview-img").removeAttribute("src");
    document.getElementById("preview-container").style.display = "none";
    dropzone.classList.remove("has-image");
    document.querySelector(".image-actions").hidden = true;
    document.getElementById("dropzone-prompt").style.display = "block";
    document.getElementById("btn-run-diagnosis").disabled = true;
    document.getElementById("image-status").textContent = "No image selected";
    setStatus("Upload an image to enable prediction.");
    const banner = document.getElementById("low-confidence-banner");
    if (banner) { banner.hidden = true; banner.textContent = ""; }
    markResultsStale();
  });

  function selectImage(file) {
    if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) {
      rejectImage("Choose a JPG, PNG, or WEBP image.");
      return;
    }
    if (file.size > 10 * 1024 * 1024) {
      rejectImage("This image is over 10 MB. Choose a smaller file.");
      return;
    }
    state.currentFile = file;
    document.querySelectorAll("#sample-leaves-container .sample-leaf-chip").forEach(button => {
      button.classList.remove("selected");
      button.setAttribute("aria-pressed", "false");
    });
    const reader = new FileReader();
    reader.onload = event => {
      document.getElementById("preview-img").src = event.target.result;
      document.getElementById("preview-container").style.display = "block";
      document.getElementById("dropzone-prompt").style.display = "none";
      dropzone.classList.add("has-image");
      document.querySelector(".image-actions").hidden = false;
      document.getElementById("preview-filename").textContent = file.name;
      document.getElementById("btn-run-diagnosis").disabled = false;
      setImageStatus(`Image ready · ${(file.size / (1024 * 1024)).toFixed(2)} MB`);
      setStatus("Image selected. Add capture metadata or keep the controlled simulation inputs.");
      markResultsStale();
    };
    reader.onerror = () => {
      rejectImage("Unable to read this image. Please choose it again.");
    };
    reader.readAsDataURL(file);
  }

  function rejectImage(message) {
    state.currentFile = null;
    fileInput.value = "";
    const camInput = document.getElementById("camera-input");
    if (camInput) camInput.value = "";
    document.getElementById("btn-run-diagnosis").disabled = true;
    document.getElementById("preview-img").removeAttribute("src");
    document.getElementById("preview-container").style.display = "none";
    document.getElementById("dropzone-prompt").style.display = "block";
    dropzone.classList.remove("has-image");
    document.querySelector(".image-actions").hidden = true;
    setImageStatus(message);
    markResultsStale();
  }
}

function initControls() {
  const sliders = [
    ["slider-temp", "val-temp", "temperature", "°C"],
    ["slider-humidity", "val-humidity", "relativeHumidity", "%"],
    ["slider-wetness", "val-wetness", "leafWetnessHours", " hrs"],
    ["slider-rain", "val-rain", "rainfallMm", " mm"],
    ["slider-wind", "val-wind", "windSpeedKmh", " km/h"],
  ];
  sliders.forEach(([inputId, labelId, stateKey, unit]) => {
    const input = document.getElementById(inputId);
    input.addEventListener("input", () => {
      state[stateKey] = Number(input.value);
      document.getElementById(labelId).textContent = `${input.value}${unit}`;
      document.querySelectorAll("#preset-chips-container .sample-chip").forEach(button => {
        button.classList.remove("selected");
        button.setAttribute("aria-pressed", "false");
      });
      markResultsStale();
    });
  });

  document.getElementById("crop-select").addEventListener("change", event => {
    state.targetCrop = event.target.value;
    markResultsStale();
  });
  document.getElementById("stage-select").addEventListener("change", event => {
    state.cropStage = event.target.value;
    markResultsStale();
  });
  ["latitude", "longitude", "observation-date"].forEach(id => {
    document.getElementById(id).addEventListener("input", () => {
      updateWeatherMode();
      markResultsStale();
    });
  });
  document.getElementById("btn-run-diagnosis").addEventListener("click", runDiagnosis);
}

function initializeWeatherMode() {
  document.getElementById("observation-date").max = new Date().toISOString().slice(0, 10);
  updateWeatherMode();
}

function updateWeatherMode() {
  const latitude = document.getElementById("latitude").value.trim();
  const longitude = document.getElementById("longitude").value.trim();
  const observationDate = document.getElementById("observation-date").value;
  const fieldCount = [latitude, longitude, observationDate].filter(Boolean).length;
  const aligned = fieldCount === 3;
  const status = document.getElementById("weather-mode-status");
  const sliders = document.querySelectorAll(".premium-slider");

  sliders.forEach(slider => {
    slider.disabled = aligned;
  });
  status.classList.toggle("is-aligned", aligned);
  status.classList.toggle("is-incomplete", fieldCount > 0 && !aligned);
  if (aligned) {
    status.textContent = "Historical weather mode · sliders are paused and these values are used for the selected date and location.";
  } else if (fieldCount > 0) {
    status.textContent = `Add ${3 - fieldCount} more ${3 - fieldCount === 1 ? "detail" : "details"} to use historical weather, or clear the fields to use simulation.`;
  } else {
    status.textContent = "Simulation mode · enter all three details above to request aligned historical weather.";
  }
}

async function initSampleLeaves() {
  const container = document.getElementById("sample-leaves-container");
  if (!container) return;
  try {
    const response = await fetch("/api/samples/leaves");
    if (!response.ok) throw new Error(`Sample leaves returned HTTP ${response.status}`);
    const samples = await response.json();
    samples.forEach(sample => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `sample-leaf-chip ${sample.is_low_conf ? "chip-warning" : ""}`;
      button.setAttribute("aria-pressed", "false");
      button.textContent = sample.badge;
      button.title = `${sample.title}: ${sample.description}`;
      button.addEventListener("click", () => loadSampleLeaf(sample, button));
      container.appendChild(button);
    });
  } catch (error) {
    console.warn("Could not load sample leaves:", error);
    setImageStatus("Unable to load sample leaves. You can still upload a photo.");
  }
}

async function loadSampleLeaf(sample, selectedButton) {
  try {
    setImageStatus(`Loading ${sample.title}…`);
    const response = await fetch(sample.file_url);
    if (!response.ok) throw new Error("Sample file could not be loaded");
    const blob = await response.blob();
    const file = new File([blob], sample.filename, { type: "image/jpeg" });
    document.querySelectorAll("#sample-leaves-container .sample-leaf-chip").forEach(button => {
      button.classList.remove("selected");
      button.setAttribute("aria-pressed", "false");
    });
    selectedButton.classList.add("selected");
    selectedButton.setAttribute("aria-pressed", "true");

    // Automatically align crop dropdown
    if (sample.crop) {
      const cropSelect = document.getElementById("crop-select");
      cropSelect.value = sample.crop;
      state.targetCrop = sample.crop;
    }

    // Populate dropzone and preview
    const dropzone = document.getElementById("dropzone");
    state.currentFile = file;
    document.getElementById("preview-img").src = URL.createObjectURL(blob);
    document.getElementById("preview-container").style.display = "block";
    document.getElementById("dropzone-prompt").style.display = "none";
    dropzone.classList.add("has-image");
    document.querySelector(".image-actions").hidden = false;
    document.getElementById("preview-filename").textContent = sample.filename;
    document.getElementById("btn-run-diagnosis").disabled = false;
    setImageStatus(`Sample ready · ${sample.title}`);
    setStatus(`Sample leaf loaded (${sample.title}). Click "Check this leaf" to run prediction.`);
    markResultsStale();
  } catch (err) {
    setImageStatus(`Failed to load sample: ${err.message}`);
  }
}

async function initWeatherPresets() {
  const container = document.getElementById("preset-chips-container");
  try {
    const response = await fetch("/api/presets/weather");
    if (!response.ok) throw new Error(`Weather presets returned HTTP ${response.status}`);
    const presets = await response.json();
    Object.values(presets).forEach(preset => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "sample-chip";
      button.setAttribute("aria-pressed", "false");
      button.textContent = preset.name;
      button.title = preset.description;
      button.addEventListener("click", () => applyPreset(preset, button));
      container.appendChild(button);
    });
  } catch (error) {
    setStatus(`Unable to load simulation presets: ${error.message}`);
    document.getElementById("prediction-status").classList.add("is-error");
  }
}

function applyPreset(preset, selectedButton) {
  const values = [
    ["slider-temp", "val-temp", "temperature", preset.temperature, "°C"],
    ["slider-humidity", "val-humidity", "relativeHumidity", preset.relative_humidity, "%"],
    ["slider-wetness", "val-wetness", "leafWetnessHours", preset.leaf_wetness_hours, " hrs"],
    ["slider-rain", "val-rain", "rainfallMm", preset.rainfall_mm, " mm"],
    ["slider-wind", "val-wind", "windSpeedKmh", preset.wind_speed_kmh, " km/h"],
  ];
  values.forEach(([inputId, labelId, stateKey, value, unit]) => {
    document.getElementById(inputId).value = value;
    document.getElementById(labelId).textContent = `${value}${unit}`;
    state[stateKey] = value;
  });
  document.getElementById("latitude").value = "";
  document.getElementById("longitude").value = "";
  document.getElementById("observation-date").value = "";
  document.querySelectorAll("#preset-chips-container .sample-chip").forEach(button => {
    button.classList.remove("selected");
    button.setAttribute("aria-pressed", "false");
  });
  selectedButton.classList.add("selected");
  selectedButton.setAttribute("aria-pressed", "true");
  updateWeatherMode();
  setStatus("Controlled simulation preset selected; no public weather observations are used.");
  markResultsStale();
}

async function runDiagnosis() {
  if (!state.currentFile) {
    setStatus("Upload a crop-leaf image before running prediction.");
    return;
  }

  const button = document.getElementById("btn-run-diagnosis");
  button.disabled = true;
  button.querySelector(".button-label").textContent = "Checking image and field details…";
  setStatus("Prediction is running.");
  button.setAttribute("aria-busy", "true");
  document.getElementById("prediction-status").classList.remove("is-error");

  try {
    const formData = new FormData();
    formData.append("file", state.currentFile);
    formData.append("temperature", state.temperature);
    formData.append("relative_humidity", state.relativeHumidity);
    formData.append("rainfall_mm", state.rainfallMm);
    formData.append("leaf_wetness_hours", state.leafWetnessHours);
    formData.append("wind_speed_kmh", state.windSpeedKmh);
    formData.append("crop_stage", state.cropStage);
    formData.append("target_crop", state.targetCrop);

    const latitude = document.getElementById("latitude").value.trim();
    const longitude = document.getElementById("longitude").value.trim();
    const observationDate = document.getElementById("observation-date").value;
    const metadataCount = [latitude, longitude, observationDate].filter(Boolean).length;
    if (metadataCount > 0 && metadataCount < 3) {
      throw new Error("Enter latitude, longitude, and image capture date together, or clear all three to use simulation.");
    }
    if (metadataCount === 3) {
      formData.append("latitude", latitude);
      formData.append("longitude", longitude);
      formData.append("observation_date", observationDate);
    }

    const response = await fetch("/api/predict/fused", { method: "POST", body: formData });
    const result = await response.json();
    if (!response.ok) {
      throw new Error(result.detail || `Prediction returned HTTP ${response.status}`);
    }
    // Fix scope bug: declare vision/environment/fusion BEFORE using them
    const vision = result.vision_details;
    const environment = result.environmental_details;
    const fusion = result.multimodal_fusion;

    state.latestResultData = result;
    renderResults(result);
    state.hasPrediction = true;
    loadScanHistory();
    state.latestPrediction = {
      predicted_class: vision.predicted_class,
      environmental_score: environment.composite_risk_score,
      fused_score: fusion.fused_risk_score,
    };
    document.getElementById("result-state-badge").textContent = "Prediction ready";
    document.getElementById("result-state-badge").classList.remove("is-stale");
    document.getElementById("results-card").classList.remove("is-stale");
    setStatus("Prediction complete. Review the source and score interpretation below.");
  } catch (error) {
    setStatus(`Prediction failed: ${error.message}`);
  } finally {
    button.disabled = !state.currentFile;
    button.querySelector(".button-label").textContent = "Check this leaf";
    button.removeAttribute("aria-busy");
  }
}

function initCropChat() {
  const form = document.getElementById("crop-chat-form");
  const input = document.getElementById("crop-chat-input");
  const sendButton = document.getElementById("crop-chat-send");
  const messages = document.getElementById("chat-messages");
  const status = document.getElementById("crop-chat-status");

  const toggleBtn = document.getElementById("chat-widget-toggle");
  const closeBtn = document.getElementById("chat-widget-close");
  const panel = document.getElementById("chat-widget-panel");
  const badge = toggleBtn ? toggleBtn.querySelector(".chat-widget-badge") : null;

  if (toggleBtn && panel) {
    toggleBtn.addEventListener("click", () => {
      const isClosed = panel.hasAttribute("hidden");
      if (isClosed) {
        panel.removeAttribute("hidden");
        toggleBtn.setAttribute("aria-expanded", "true");
        if (badge) badge.style.display = "none";
        setTimeout(() => input.focus(), 100);
        messages.scrollTop = messages.scrollHeight;
      } else {
        panel.setAttribute("hidden", "");
        toggleBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  if (closeBtn && panel) {
    closeBtn.addEventListener("click", () => {
      panel.setAttribute("hidden", "");
      if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
    });
  }

  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && panel && !panel.hasAttribute("hidden")) {
      panel.setAttribute("hidden", "");
      if (toggleBtn) toggleBtn.setAttribute("aria-expanded", "false");
      toggleBtn.focus();
    }
  });

  form.addEventListener("submit", async event => {
    event.preventDefault();
    const message = input.value.trim();
    if (!message) return;

    appendChatMessage(message, "user-message");
    input.value = "";
    sendButton.disabled = true;
    status.textContent = "Assistant is preparing an answer…";
    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message,
          ...(state.latestPrediction || {}),
        }),
      });
      const result = await response.json();
      if (!response.ok) {
        throw new Error(result.detail || `Chat returned HTTP ${response.status}`);
      }
      appendChatMessage(result.answer, "assistant-message");
      status.textContent = result.disclaimer;
    } catch (error) {
      status.textContent = `Unable to get a response: ${error.message}`;
      status.classList.add("is-error");
    } finally {
      sendButton.disabled = false;
      input.focus();
    }
  });

  function appendChatMessage(text, className) {
    const message = document.createElement("div");
    message.className = `chat-message ${className}`;
    message.textContent = text;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
  }
}

function renderResults(result) {
  const fusion = result.multimodal_fusion;
  const vision = result.vision_details;
  const environment = result.environmental_details;
  const score = fusion.fused_risk_score;
  const riskLevel = score >= 75 ? "higher" : score >= 45 ? "moderate" : "lower";
  document.getElementById("results-card").classList.add("has-result");
  document.getElementById("guidance").classList.add("has-result");

  const summaryTitle = document.getElementById("result-summary-title");
  const summaryCopy = document.getElementById("result-summary-copy");
  if (vision.confidence_status === "low_confidence") {
    summaryTitle.textContent = "No clear image match";
    summaryCopy.textContent =
      "The image model could not make a reliable match. Review the other possible matches below, or try a sharply focused photo of one leaf in good light. The combined risk index is not a probability of disease.";
  } else if (fusion.is_healthy) {
    summaryTitle.textContent = "No disease pattern identified in the photo";
    summaryCopy.textContent =
      `The image model's closest match is healthy ${fusion.crop} foliage. The ${riskLevel} combined risk index describes the image and field-condition inputs; it does not mean a disease is present. Continue monitoring and compare the notes below.`;
  } else {
    summaryTitle.textContent = `Possible image match: ${fusion.disease_name}`;
    summaryCopy.textContent =
      `The photo most closely matches ${fusion.disease_name}. The combined risk index is ${Math.round(score)}% (${riskLevel}); it combines image evidence with field conditions and is not a probability of infection. Compare the symptoms below and seek local confirmation before treatment.`;
  }

  // ── Low-confidence state (P05-A) ─────────────────────────────────────────
  const isLowConf = vision.confidence_status === "low_confidence";
  const lowConfBanner = document.getElementById("low-confidence-banner");
  if (lowConfBanner) {
    lowConfBanner.hidden = !isLowConf;
    if (isLowConf && vision.low_confidence_message) {
      lowConfBanner.textContent = `⚠ ${vision.low_confidence_message}`;
    } else {
      lowConfBanner.textContent = "";
    }
  }

  // ── Risk gauge ────────────────────────────────────────────────────────────
  document.getElementById("gauge-number").textContent = `${Math.round(score)}%`;
  document.getElementById("gauge-circle-progress").style.strokeDashoffset =
    314.2 - (Math.min(100, Math.max(0, score)) / 100) * 314.2;
  const gauge = document.getElementById("gauge-circle-progress");
  gauge.style.stroke = score >= 75 ? "var(--risk-high)" : score >= 45 ? "var(--risk-medium)" : "var(--risk-low)";
  document.querySelector(".circular-progress").setAttribute(
    "aria-label",
    `Combined risk index ${Math.round(score)} percent`
  );

  // ── Disease name: do NOT show a single bold name when low confidence ──────
  const diseaseNameEl = document.getElementById("res-disease-name");
  if (isLowConf) {
    diseaseNameEl.textContent = "Uncertain — see other matches";
    diseaseNameEl.style.opacity = "";
    document.querySelector(".result-overline").textContent = "Image match needs review";
  } else if (fusion.is_healthy) {
    diseaseNameEl.textContent = `Healthy ${fusion.crop} leaf`;
    diseaseNameEl.style.opacity = "";
    document.querySelector(".result-overline").textContent = "Most likely image match";
  } else {
    diseaseNameEl.textContent = fusion.disease_name;
    diseaseNameEl.style.opacity = "";
    document.querySelector(".result-overline").textContent = "Most likely image match";
  }
  document.getElementById("tag-pathogen").textContent = fusion.pathogen_type;
  document.getElementById("tag-crop").textContent = fusion.crop;
  document.getElementById("tag-urgency").textContent = `Risk index: ${riskLevel}`;
  document.getElementById("tag-urgency").title = fusion.urgency_level;
  document.getElementById("vision-confidence").textContent =
    `${vision.percentage}% · ${vision.engine}`;
  document.getElementById("top-k-description").textContent =
    `Model scores for ${fusion.crop}; review the top result with the image. These are not validated probabilities.`;

  // ── Top-3 predictions (always show) ──────────────────────────────────────
  renderTopPredictions(vision.top_k ? vision.top_k.slice(0, 3) : []);

  // ── Fusion contribution bars (P05-B transparency) ─────────────────────────
  renderFusionBars(fusion);

  // ── Weather source labeling (P05-C) ───────────────────────────────────────
  const source = environment.data_source;
  const weatherSource = environment.weather_source || "simulated";
  const isSimulated = weatherSource === "simulated";
  const simTag = document.getElementById("simulated-weather-tag");
  if (simTag) simTag.hidden = !isSimulated;

  const alignment = source.spatially_aligned
    ? `Aligned to ${source.latitude}, ${source.longitude} on ${source.observation_date} (UTC).`
    : source.notice;
  const wetnessNote = source.leaf_wetness
    ? ` Leaf wetness (estimated): ${source.leaf_wetness}.`
    : "";
  const sourceLabel = isSimulated
    ? "⚠ Simulated weather — "
    : `Source: ${source.name}. `;
  document.getElementById("environmental-result-copy").textContent =
    `Environmental favorability index: ${environment.composite_risk_score}% — ${environment.severity_level}. ` +
    `${sourceLabel}${alignment}${wetnessNote} ${environment.score_interpretation} ` +
    `Guidance only — not a confirmed diagnosis.`;

  renderList("res-reasoning-list", fusion.reasoning_summary);
  renderList("res-symptoms-list", fusion.symptoms_identified);
  renderTreatmentPlan(fusion.treatment_plan);
}

/**
 * Render fusion contribution bars (photo evidence vs field conditions).
 * Shows how much each part contributed to the risk index. (P05-B)
 */
function renderFusionBars(fusion) {
  const container = document.getElementById("fusion-bars-container");
  if (!container) return;
  const visionPct = fusion.vision_contribution ?? null;
  const envPct = fusion.environment_contribution ?? null;
  if (visionPct === null && envPct === null) { container.hidden = true; return; }
  container.hidden = false;
  container.innerHTML = `
    <p class="fusion-bars-label">How the risk index was built
      <span class="fusion-note">(heuristic weights, not calibrated)</span>
    </p>
    <div class="fusion-bar-row">
      <span class="fusion-bar-name">Photo evidence</span>
      <div class="fusion-bar-track">
        <div class="fusion-bar-fill fusion-vision" style="width:${Math.min(100, visionPct ?? 0)}%"></div>
      </div>
      <span class="fusion-bar-value">${visionPct ?? "—"}%</span>
    </div>
    <div class="fusion-bar-row">
      <span class="fusion-bar-name">Field conditions</span>
      <div class="fusion-bar-track">
        <div class="fusion-bar-fill fusion-env" style="width:${Math.min(100, envPct ?? 0)}%"></div>
      </div>
      <span class="fusion-bar-value">${envPct ?? "—"}%</span>
    </div>
    <p class="fusion-disclaimer">Guidance only — not a confirmed diagnosis.</p>
  `;
}

function renderList(elementId, values) {
  const list = document.getElementById(elementId);
  list.replaceChildren();
  (values || []).forEach(value => {
    const item = document.createElement("li");
    item.textContent = value;
    list.appendChild(item);
  });
}

function renderTreatmentPlan(plan) {
  renderTreatmentItems("plan-immediate", plan.immediate_interventions, item => item);
  renderTreatmentItems("plan-organic", plan.organic_remedies, item =>
    `${item.name} — dosage: ${item.dosage}; frequency: ${item.frequency}; PHI: ${item.phi_days} days`
  );
  renderTreatmentItems("plan-chemical", plan.chemical_controls, item =>
    `${item.name} — dosage: ${item.dosage}; frequency: ${item.frequency}; PHI: ${item.phi_days} days`
  );
  const cultural = document.getElementById("plan-cultural");
  cultural.replaceChildren();
  const guidance = document.createElement("p");
  guidance.textContent = plan.cultural_guidance || "Continue routine field scouting.";
  cultural.appendChild(guidance);
}

function renderTreatmentItems(elementId, values, format) {
  const container = document.getElementById(elementId);
  container.replaceChildren();
  if (!values || values.length === 0) {
    const empty = document.createElement("p");
    empty.textContent = "No specific intervention is listed for this result.";
    container.appendChild(empty);
    return;
  }
  values.forEach(value => {
    const item = document.createElement("div");
    item.className = "treatment-card";
    item.textContent = format(value);
    container.appendChild(item);
  });
}

function renderTopPredictions(topK) {
  const container = document.getElementById("top-predictions-container");
  container.replaceChildren();
  (topK || []).forEach((prediction, index) => {
    const row = document.createElement("div");
    row.className = "top-prediction-row";

    const label = document.createElement("span");
    label.className = "top-pred-label";
    label.textContent = `${index + 1}. ${prediction.display_name}`;

    const track = document.createElement("div");
    track.className = "top-pred-bar-track";
    const fill = document.createElement("div");
    fill.className = "top-pred-bar-fill";
    fill.style.width = `${Math.min(100, prediction.percentage)}%`;
    track.appendChild(fill);

    const score = document.createElement("span");
    score.className = "top-pred-score";
    score.textContent = `${prediction.percentage}%`;

    row.appendChild(label);
    row.appendChild(track);
    row.appendChild(score);
    container.appendChild(row);
  });
}

function initPlanTabs() {
  const buttons = document.querySelectorAll(".plan-tab-btn");
  const sections = document.querySelectorAll(".plan-section");
  buttons.forEach((button, index) => {
    button.addEventListener("click", () => {
      selectTab(button);
    });
    button.addEventListener("keydown", event => {
      if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
      event.preventDefault();
      const nextIndex = event.key === "Home" ? 0
        : event.key === "End" ? buttons.length - 1
        : (index + (event.key === "ArrowRight" ? 1 : buttons.length - 1)) % buttons.length;
      buttons[nextIndex].focus();
      selectTab(buttons[nextIndex]);
    });
  });

  function selectTab(selectedButton) {
    buttons.forEach(item => {
      const selected = item === selectedButton;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-selected", String(selected));
      item.tabIndex = selected ? 0 : -1;
    });
    sections.forEach(item => {
      const selected = item.id === selectedButton.dataset.target;
      item.classList.toggle("active", selected);
      item.hidden = !selected;
    });
  }
}

function setStatus(message) {
  const status = document.getElementById("prediction-status");
  status.textContent = message;
  status.classList.toggle("is-error", message.startsWith("Prediction failed:") || message.startsWith("Enter "));
}

function setImageStatus(message) {
  const status = document.getElementById("image-status");
  status.textContent = message;
  status.classList.toggle("is-error", message.startsWith("Choose ") || message.startsWith("This image") || message.startsWith("Unable") || message.startsWith("Failed"));
}

function markResultsStale() {
  if (!state.hasPrediction) return;
  document.getElementById("result-state-badge").textContent =
    state.currentFile ? "Inputs changed · rerun" : "Previous result";
  document.getElementById("result-state-badge").classList.add("is-stale");
  document.getElementById("results-card").classList.add("is-stale");
}

function initScrollSpy() {
  const links = [...document.querySelectorAll(".nav-link, .mobile-nav a")];
  const sections = ["home", "diagnose", "guidance"].map(id => document.getElementById(id)).filter(Boolean);
  if ("IntersectionObserver" in window && sections.length > 0) {
    const spy = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.toggle("active", a.getAttribute("href") === `#${entry.target.id}`));
      });
    }, { rootMargin: "-30% 0px -55% 0px" });
    sections.forEach(s => spy.observe(s));
  }
}

function initClipboardPaste() {
  document.addEventListener("paste", event => {
    // If user is focused on text input and not pasting an image, let default paste proceed
    const items = event.clipboardData?.items;
    if (!items) return;
    for (let i = 0; i < items.length; i++) {
      if (items[i].type.startsWith("image/")) {
        const file = items[i].getAsFile();
        if (file) {
          event.preventDefault();
          const input = document.getElementById("file-input");
          if (input) {
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            input.dispatchEvent(new Event("change", { bubbles: true }));
          }
          break;
        }
      }
    }
  });
}

function initMobileResultFocus() {
  const badge = document.getElementById("result-state-badge");
  if (badge) {
    new MutationObserver(() => {
      if (badge.textContent.includes("ready") && window.matchMedia("(max-width: 960px)").matches) {
        document.getElementById("results-card")?.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    }).observe(badge, { childList: true, characterData: true, subtree: true });
  }
}


/* ==========================================================================
   Language Switcher Implementation (English & Hindi)
   ========================================================================== */
function initLanguageSwitcher() {
  const btnEn = document.getElementById("btn-lang-en");
  const btnHi = document.getElementById("btn-lang-hi");
  if (!btnEn || !btnHi) return;

  btnEn.addEventListener("click", () => switchLanguage("en"));
  btnHi.addEventListener("click", () => switchLanguage("hi"));
}

function switchLanguage(lang) {
  state.currentLanguage = lang;
  const btnEn = document.getElementById("btn-lang-en");
  const btnHi = document.getElementById("btn-lang-hi");
  if (btnEn && btnHi) {
    btnEn.classList.toggle("active", lang === "en");
    btnEn.setAttribute("aria-pressed", lang === "en");
    btnHi.classList.toggle("active", lang === "hi");
    btnHi.setAttribute("aria-pressed", lang === "hi");
  }

  const dict = TRANSLATIONS[lang] || TRANSLATIONS.en;
  document.querySelectorAll("[data-i18n]").forEach(el => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      if (dict[key].includes("<") && dict[key].includes(">")) {
        el.innerHTML = dict[key];
      } else {
        el.textContent = dict[key];
      }
    }
  });

  const chatInput = document.getElementById("crop-chat-input");
  if (chatInput) {
    chatInput.placeholder = lang === "hi" ? "अपनी फसल के बारे में पूछें…" : "Ask about your crop…";
  }

  loadScanHistory();
  updateSpeakButtonState();
}

/* ==========================================================================
   Web Speech Audio Guidance (Text-to-Speech)
   ========================================================================== */
function initAudioGuidance() {
  const speakBtn = document.getElementById("btn-speak-guidance");
  if (!speakBtn) return;
  speakBtn.addEventListener("click", () => speakGuidance());
}

function updateSpeakButtonState() {
  const speakBtn = document.getElementById("btn-speak-guidance");
  const label = document.getElementById("speak-label");
  const icon = document.getElementById("speak-icon");
  if (!speakBtn || !label || !icon) return;

  const dict = TRANSLATIONS[state.currentLanguage] || TRANSLATIONS.en;
  if (state.isSpeaking) {
    speakBtn.classList.add("is-speaking");
    label.textContent = dict.btn_stop_listen;
    icon.textContent = "⏹";
  } else {
    speakBtn.classList.remove("is-speaking");
    label.textContent = dict.btn_listen;
    icon.textContent = "🔊";
  }
}

function speakGuidance() {
  if (!("speechSynthesis" in window)) {
    alert("Speech synthesis is not supported in this browser.");
    return;
  }
  const synth = window.speechSynthesis;
  if (state.isSpeaking) {
    synth.cancel();
    state.isSpeaking = false;
    updateSpeakButtonState();
    return;
  }

  if (!state.hasPrediction || !state.latestResultData) {
    const emptyMsg = state.currentLanguage === "hi"
      ? "कृपया उपचार सलाह सुनने के लिए पहले पत्ती की जांच करें।"
      : "Please run a crop check first to listen to treatment guidance.";
    const utt = new SpeechSynthesisUtterance(emptyMsg);
    utt.lang = state.currentLanguage === "hi" ? "hi-IN" : "en-US";
    synth.speak(utt);
    return;
  }

  const fusion = state.latestResultData.multimodal_fusion;
  const isHealthy = fusion.is_healthy;
  const disease = fusion.disease_name;
  const urgency = fusion.urgency_level;
  const treatments = fusion.treatment_plan || {};

  let textToSpeak = "";
  if (state.currentLanguage === "hi") {
    if (isHealthy) {
      textToSpeak = `आपकी फसल ${disease} स्वस्थ पाई गई है। किसी रासायनिक कीटनाशक की आवश्यकता नहीं है। नियमित सिंचाई और पोषण बनाए रखें।`;
    } else {
      const immediate = (treatments.immediate_interventions || []).slice(0, 2).join(". ");
      const organic = (treatments.organic_remedies || []).map(o => o.name).slice(0, 2).join(", ");
      textToSpeak = `जांच परिणाम: ${disease}। जोखिम स्तर: ${urgency}। प्राथमिक कदम: ${immediate}। अनुशंसित जैविक उपचार: ${organic || "खेत स्वच्छता रखें"}। रासायनिक प्रयोग से पहले स्थानीय कृषि अधिकारी से पुष्टि करें।`;
    }
  } else {
    if (isHealthy) {
      textToSpeak = `Your crop ${disease} is assessed as healthy. No chemical controls are required. Maintain routine irrigation and field scouting.`;
    } else {
      const immediate = (treatments.immediate_interventions || []).slice(0, 2).join(". ");
      const organic = (treatments.organic_remedies || []).map(o => o.name).slice(0, 2).join(", ");
      textToSpeak = `Diagnosis result: ${disease}. Urgency level: ${urgency}. Initial interventions: ${immediate}. Organic remedies: ${organic || "Maintain field sanitation"}. Always confirm chemical treatments with a local advisor.`;
    }
  }

  const utterance = new SpeechSynthesisUtterance(textToSpeak);
  utterance.lang = state.currentLanguage === "hi" ? "hi-IN" : "en-US";
  utterance.rate = 0.95;
  utterance.onstart = () => {
    state.isSpeaking = true;
    updateSpeakButtonState();
  };
  utterance.onend = () => {
    state.isSpeaking = false;
    updateSpeakButtonState();
  };
  utterance.onerror = () => {
    state.isSpeaking = false;
    updateSpeakButtonState();
  };
  synth.speak(utterance);
}

/* ==========================================================================
   Scan History Implementation (SQLite-backed)
   ========================================================================== */
function initScanHistory() {
  const clearBtn = document.getElementById("btn-clear-history");
  if (clearBtn) {
    clearBtn.addEventListener("click", async () => {
      try {
        await fetch("/api/history", { method: "DELETE" });
        loadScanHistory();
      } catch (err) {
        console.error("Failed to clear history:", err);
      }
    });
  }
  loadScanHistory();
}

async function loadScanHistory() {
  const container = document.getElementById("history-list");
  if (!container) return;
  try {
    const res = await fetch("/api/history?limit=10");
    if (!res.ok) return;
    const records = await res.json();
    const dict = TRANSLATIONS[state.currentLanguage] || TRANSLATIONS.en;
    if (!records || records.length === 0) {
      container.innerHTML = `<p class="history-empty">${dict.history_empty}</p>`;
      return;
    }
    container.innerHTML = records.map(r => {
      const dt = new Date(r.timestamp);
      const timeStr = dt.toLocaleDateString() + " " + dt.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      const badgeClass = r.confidence_status === "ok" ? "crop-tag" : "urgency-tag";
      const riskColor = r.risk_score >= 70 ? "#ef4444" : r.risk_score >= 40 ? "#f97316" : "#22c55e";
      const weatherLabel = r.weather_source === "open-meteo" ? "Aligned Weather" : "Simulation";
      return `
        <div class="history-item">
          <div class="history-main">
            <span class="history-title">${r.disease_name}</span>
            <div class="history-meta">
              <span class="history-badge ${badgeClass}">${r.crop}</span>
              <span>${timeStr}</span>
              <span>· ${(r.confidence * 100).toFixed(1)}% match</span>
              <span>· ${weatherLabel}</span>
            </div>
          </div>
          <div class="history-score" style="color: ${riskColor};">
            ${r.risk_score}<span style="font-size: 10px; color: var(--color-secondary-text);">/100</span>
          </div>
        </div>
      `;
    }).join("");
  } catch (err) {
    console.error("Failed to load history:", err);
  }
}
