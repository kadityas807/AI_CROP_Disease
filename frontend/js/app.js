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
});

function initUpload() {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");

  dropzone.addEventListener("click", () => fileInput.click());
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
  document.getElementById("remove-image").addEventListener("click", event => {
    state.currentFile = null;
    fileInput.value = "";
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
    if (!response.ok) return;
    const samples = await response.json();
    samples.forEach(sample => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = `sample-leaf-chip ${sample.is_low_conf ? "chip-warning" : ""}`;
      button.textContent = sample.badge;
      button.title = `${sample.title}: ${sample.description}`;
      button.addEventListener("click", () => loadSampleLeaf(sample));
      container.appendChild(button);
    });
  } catch (error) {
    console.warn("Could not load sample leaves:", error);
  }
}

async function loadSampleLeaf(sample) {
  try {
    setImageStatus(`Loading ${sample.title}…`);
    const response = await fetch(sample.file_url);
    if (!response.ok) throw new Error("Sample file could not be loaded");
    const blob = await response.blob();
    const file = new File([blob], sample.filename, { type: "image/jpeg" });

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
      button.textContent = preset.name;
      button.title = preset.description;
      button.addEventListener("click", () => applyPreset(preset));
      container.appendChild(button);
    });
  } catch (error) {
    setStatus(`Unable to load simulation presets: ${error.message}`);
  }
}

function applyPreset(preset) {
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

    renderResults(result);
    state.hasPrediction = true;
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
    const message = document.createElement("p");
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
  document.getElementById("tag-pathogen").textContent = `🔬 ${fusion.pathogen_type}`;
  document.getElementById("tag-crop").textContent = `🌱 ${fusion.crop}`;
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
      <span class="fusion-bar-name">📷 Photo evidence</span>
      <div class="fusion-bar-track">
        <div class="fusion-bar-fill fusion-vision" style="width:${Math.min(100, visionPct ?? 0)}%"></div>
      </div>
      <span class="fusion-bar-value">${visionPct ?? "—"}%</span>
    </div>
    <div class="fusion-bar-row">
      <span class="fusion-bar-name">🌦 Field conditions</span>
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
  buttons.forEach(button => {
    button.addEventListener("click", () => {
      buttons.forEach(item => item.classList.remove("active"));
      sections.forEach(item => item.classList.remove("active"));
      button.classList.add("active");
      document.getElementById(button.dataset.target).classList.add("active");
    });
  });
}

function setStatus(message) {
  const status = document.getElementById("prediction-status");
  status.textContent = message;
  status.classList.toggle("is-error", message.startsWith("Prediction failed:") || message.startsWith("Enter "));
}

function setImageStatus(message) {
  const status = document.getElementById("image-status");
  status.textContent = message;
  status.classList.toggle("is-error", message.startsWith("Choose ") || message.startsWith("This image") || message.startsWith("Unable"));
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
