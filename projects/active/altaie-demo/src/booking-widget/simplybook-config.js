/**
 * SimplyBook Widget Configuration
 * Gjenbrukbar config for alle frisør-kunder
 */

const SimplyBookConfig = {
  // Bytt ut med kundens SimplyBook URL
  // Format: https://[salong-navn].simplybook.me
  widgetUrl: 'https://altaiefrisor.simplybook.me/v2/',
  
  // Tilpasninger
  theme: {
    primaryColor: '#667eea',      // Hovedfarge (kan endres per kunde)
    secondaryColor: '#764ba2',    // Sekundærfarge
    buttonColor: '#667eea',       // Knapp-farge
    fontFamily: 'Segoe UI, sans-serif'
  },
  
  // Tjenester (hentes automatisk fra SimplyBook, men kan overstyres)
  services: [
    { id: '1', name: 'Herreklipp', duration: '30 min', price: '350 kr' },
    { id: '2', name: 'Dameklipp', duration: '45 min', price: '450 kr' },
    { id: '3', name: 'Farging', duration: '90 min', price: '800 kr' },
    { id: '4', name: 'Striper', duration: '120 min', price: '1200 kr' }
  ],
  
  // Åpningstider (for visning)
  openingHours: {
    monday: '09:00 - 17:00',
    tuesday: '09:00 - 17:00',
    wednesday: '09:00 - 17:00',
    thursday: '09:00 - 17:00',
    friday: '09:00 - 17:00',
    saturday: '10:00 - 14:00',
    sunday: 'Stengt'
  }
};

// Export for bruk i andre filer
if (typeof module !== 'undefined' && module.exports) {
  module.exports = SimplyBookConfig;
}
