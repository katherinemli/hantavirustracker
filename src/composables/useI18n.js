import { ref } from 'vue'

/* Singleton compartido por todos los componentes */
const locale = ref('es')

const MESSAGES = {
  es: {
    title:    'Monitor Hantavirus Andes',
    abbr:     '(ANDV)',
    org:      'OMS · CDC · ECDC · Vigilancia Global',
    updated:  'Actualizado',
    // Stats
    confirmed:  'Confirmados',
    monitoring: 'En monitoreo',
    countries:  'Países con alerta',
    // Left sidebar
    filters:            'Filtros',
    all:                'Todos',
    filter_confirmed:   'Confirmado',
    filter_monitoring:  'Monitoreo',
    search_placeholder: 'Buscar país…',
    case_register:      'Registro de casos',
    no_cases:           'Sin casos para el filtro seleccionado.',
    col_country: 'País',
    col_date:    'Fecha',
    col_status:  'Estado',
    col_source:  'Fuente',
    // Right sidebar
    recent_activity: 'Actividad reciente',
    no_news:         'Sin entradas disponibles.',
    view_source:     'Ver fuente ↗',
    // Map
    ship_route:  'Ruta estimada MV Hondius',
    cases_label: 'Casos ANDV',
    // Status
    status_confirmed:  'Confirmado',
    status_monitoring: 'Monitoreo',
    // Footer
    disclaimer: 'Datos verificados por agencias internacionales. Foco: Brote asociado a pasajeros del MV Hondius.',
    // App states
    loading:      'Cargando datos…',
    error_prefix: 'Error al cargar:',
  },
  en: {
    title:    'Hantavirus Andes Monitor',
    abbr:     '(ANDV)',
    org:      'WHO · CDC · ECDC · Global Surveillance',
    updated:  'Updated',
    confirmed:  'Confirmed',
    monitoring: 'Under Monitoring',
    countries:  'Countries on Alert',
    filters:            'Filters',
    all:                'All',
    filter_confirmed:   'Confirmed',
    filter_monitoring:  'Monitoring',
    search_placeholder: 'Search country…',
    case_register:      'Case Registry',
    no_cases:           'No cases for the selected filter.',
    col_country: 'Country',
    col_date:    'Date',
    col_status:  'Status',
    col_source:  'Source',
    recent_activity: 'Recent Activity',
    no_news:         'No entries available.',
    view_source:     'View source ↗',
    ship_route:  'Estimated MV Hondius Route',
    cases_label: 'ANDV Cases',
    status_confirmed:  'Confirmed',
    status_monitoring: 'Monitoring',
    disclaimer: 'Data verified by international agencies. Focus: Outbreak associated with MV Hondius passengers.',
    loading:      'Loading data…',
    error_prefix: 'Error loading:',
  },
  fr: {
    title:    'Moniteur Hantavirus Andes',
    abbr:     '(ANDV)',
    org:      'OMS · CDC · ECDC · Surveillance Mondiale',
    updated:  'Mis à jour',
    confirmed:  'Confirmés',
    monitoring: 'Sous surveillance',
    countries:  'Pays en alerte',
    filters:            'Filtres',
    all:                'Tous',
    filter_confirmed:   'Confirmé',
    filter_monitoring:  'Surveillance',
    search_placeholder: 'Rechercher un pays…',
    case_register:      'Registre des cas',
    no_cases:           'Aucun cas pour le filtre sélectionné.',
    col_country: 'Pays',
    col_date:    'Date',
    col_status:  'Statut',
    col_source:  'Source',
    recent_activity: 'Activité récente',
    no_news:         'Aucune entrée disponible.',
    view_source:     'Voir la source ↗',
    ship_route:  'Route estimée MV Hondius',
    cases_label: 'Cas ANDV',
    status_confirmed:  'Confirmé',
    status_monitoring: 'Surveillance',
    disclaimer: 'Données vérifiées par des agences internationales. Focus: Épidémie liée aux passagers du MV Hondius.',
    loading:      'Chargement…',
    error_prefix: 'Erreur de chargement:',
  },
}

export function useI18n() {
  const t = (key) => MESSAGES[locale.value]?.[key] ?? MESSAGES.es[key] ?? key
  return { locale, t }
}
