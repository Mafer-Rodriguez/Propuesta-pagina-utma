/** Tokens de marca UTMA (extraídos del logotipo institucional) */
module.exports = {
  content: ['./*.html', './carreras/*.html', './noticias/*.html', './js/*.js'],
  theme: {
    extend: {
      colors: {
        ink: '#1D191A',
        navy: { DEFAULT: '#235F83', deep: '#173F57', soft: '#E6F0F5' },
        ut: { DEFAULT: '#00785F', brand: '#00A884', soft: '#E3F5EF' },
        naranja: { DEFAULT: '#F57E26', text: '#A84A08', soft: '#FFF0E4' },
        carmin: '#B61F3E', sol: '#FDC24E', coral: '#F2705A', aqua: '#35BAA4', salvia: '#81B4B8',
        paper: '#F6F8F9'
      },
      fontFamily: {
        display: ['"Bricolage Grotesque"', 'ui-sans-serif', 'system-ui', 'sans-serif'],
        sans: ['"Atkinson Hyperlegible"', 'ui-sans-serif', 'system-ui', 'Segoe UI', 'Roboto', 'sans-serif']
      }
    }
  }
};
