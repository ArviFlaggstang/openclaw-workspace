/**
 * Booking Widget med SimplyBook integrasjon
 * Enkel, gjenbrukbar løsning for frisører
 */

class BookingWidget {
  constructor(config) {
    this.config = config;
    this.selectedService = null;
    this.selectedDate = null;
    this.selectedTime = null;
  }

  // Initialiser widget
  init() {
    this.renderForm();
    this.attachEventListeners();
  }

  // Render booking-skjema
  renderForm() {
    const container = document.getElementById('booking-widget');
    if (!container) return;

    container.innerHTML = `
      <div class="booking-form">
        <h3>Bestill time</h3>
        <p class="subtitle">Velg tjeneste, dato og tid</p>
        
        <!-- Steg 1: Velg tjeneste -->
        <div class="form-step" id="step-1">
          <label>Tjeneste *</label>
          <select id="service-select" required>
            <option value="">Velg tjeneste</option>
            ${this.config.services.map(s => `
              <option value="${s.id}" data-duration="${s.duration}" data-price="${s.price}">
                ${s.name} - ${s.price} (${s.duration})
              </option>
            `).join('')}
          </select>
        </div>

        <!-- Steg 2: Velg dato -->
        <div class="form-step" id="step-2" style="display:none;">
          <label>Ønsket dato *</label>
          <input type="date" id="date-select" required min="${this.getToday()}">
        </div>

        <!-- Steg 3: Velg tid -->
        <div class="form-step" id="step-3" style="display:none;">
          <label>Ønsket tid *</label>
          <select id="time-select" required>
            <option value="">--:--</option>
            ${this.generateTimeSlots()}
          </select>
        </div>

        <!-- Steg 4: Kontaktinfo -->
        <div class="form-step" id="step-4" style="display:none;">
          <label>Ditt fulle navn *</label>
          <input type="text" id="customer-name" placeholder="Navn" required>
          
          <label>Telefon *</label>
          <input type="tel" id="customer-phone" placeholder="+47 XXX XX XXX" required>
          
          <label>E-post</label>
          <input type="email" id="customer-email" placeholder="valgfritt">
        </div>

        <!-- Neste/Fullfør knapp -->
        <button type="button" id="next-btn" class="btn-primary">
          Neste
        </button>

        <!-- SimplyBook iframe (vises til slutt) -->
        <div id="simplybook-container" style="display:none; margin-top:20px;">
          <p>Du videreføres til vårt booking-system...</p>
          <iframe 
            id="simplybook-iframe"
            src="" 
            width="100%" 
            height="600" 
            frameborder="0">
          </iframe>
        </div>
      </div>
    `;
  }

  // Generer tidslotter
  generateTimeSlots() {
    const slots = [];
    const startHour = 9;
    const endHour = 17;
    
    for (let hour = startHour; hour < endHour; hour++) {
      slots.push(`<option value="${hour}:00">${hour}:00</option>`);
      slots.push(`<option value="${hour}:30">${hour}:30</option>`);
    }
    return slots.join('');
  }

  // Hent dagens dato
  getToday() {
    return new Date().toISOString().split('T')[0];
  }

  // Event listeners
  attachEventListeners() {
    const nextBtn = document.getElementById('next-btn');
    if (!nextBtn) return;

    let currentStep = 1;

    nextBtn.addEventListener('click', () => {
      if (this.validateStep(currentStep)) {
        currentStep++;
        this.showStep(currentStep);
        
        if (currentStep === 5) {
          this.redirectToSimplyBook();
        }
      }
    });

    // Vis neste steg når forrige er fylt ut
    document.getElementById('service-select')?.addEventListener('change', () => {
      document.getElementById('step-2').style.display = 'block';
    });

    document.getElementById('date-select')?.addEventListener('change', () => {
      document.getElementById('step-3').style.display = 'block';
    });

    document.getElementById('time-select')?.addEventListener('change', () => {
      document.getElementById('step-4').style.display = 'block';
    });
  }

  // Valider hvert steg
  validateStep(step) {
    switch(step) {
      case 1:
        return document.getElementById('service-select').value !== '';
      case 2:
        return document.getElementById('date-select').value !== '';
      case 3:
        return document.getElementById('time-select').value !== '';
      case 4:
        const name = document.getElementById('customer-name').value;
        const phone = document.getElementById('customer-phone').value;
        return name !== '' && phone !== '';
      default:
        return true;
    }
  }

  // Vis steg
  showStep(step) {
    const stepDiv = document.getElementById(`step-${step}`);
    if (stepDiv) {
      stepDiv.style.display = 'block';
      stepDiv.scrollIntoView({ behavior: 'smooth' });
    }

    // Endre knappetekst på siste steg
    const nextBtn = document.getElementById('next-btn');
    if (step === 4) {
      nextBtn.textContent = 'Fullfør booking →';
    }
  }

  // Redirect til SimplyBook med forhåndsutfylt info
  redirectToSimplyBook() {
    const service = document.getElementById('service-select').value;
    const date = document.getElementById('date-select').value;
    const time = document.getElementById('time-select').value;
    const name = document.getElementById('customer-name').value;
    const phone = document.getElementById('customer-phone').value;
    const email = document.getElementById('customer-email').value;

    // Bygg SimplyBook URL med parametere
    const params = new URLSearchParams({
      service: service,
      date: date,
      time: time,
      name: name,
      phone: phone,
      email: email
    });

    const simplybookUrl = `${this.config.widgetUrl}?${params.toString()}`;

    // Vis iframe
    document.getElementById('simplybook-container').style.display = 'block';
    document.getElementById('simplybook-iframe').src = simplybookUrl;
    document.getElementById('next-btn').style.display = 'none';

    // Scroll til iframe
    document.getElementById('simplybook-container').scrollIntoView({ behavior: 'smooth' });
  }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
  module.exports = BookingWidget;
}
