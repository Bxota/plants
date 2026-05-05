/**
 * Derive a 1-5 numeric level from a care text field.
 * Used as fallback when plant.levels is null.
 */
export function textToLevel(text, type) {
  if (!text) return 3
  const t = text.toLowerCase()
  switch (type) {
    case 'water':
      if (t.includes('jamais') || t.includes('très rare')) return 1
      if (t.includes('peu') || t.includes('rare') || t.includes('séch')) return 2
      if (t.includes('fréquent') || t.includes('régulier')) return 4
      if (t.includes('abond') || t.includes('beaucoup') || t.includes('2 fois')) return 5
      return 3
    case 'light':
      if (t.includes('faible') || t.includes('ombre') || t.includes('tamisé')) return 2
      if (t.includes('indirecte') || t.includes('mi-ombre')) return 3
      if (t.includes('vive') || t.includes('forte')) return 4
      if (t.includes('plein soleil') || t.includes('directe')) return 5
      return 3
    case 'temp':
      if (t.includes('frais') || t.includes('froid')) return 2
      if (t.includes('chaud') || t.includes('tropical')) return 4
      return 3
    case 'humidity':
      if (t.includes('très faible') || t.includes('sec') || t.includes('aride')) return 1
      if (t.includes('faible')) return 2
      if (t.includes('très élevée') || t.includes('très haute')) return 5
      if (t.includes('élevée') || t.includes('haute')) return 4
      if (t.includes('modér')) return 3
      return 3
    case 'fertilizer':
      if (t.includes('jamais') || t.includes('rarement')) return 1
      if (t.includes('mensuel') || t.includes('mois')) return 2
      if (t.includes('bi-') || t.includes('deux fois')) return 3
      if (t.includes('régulier') || t.includes('fréquent')) return 4
      return 2
    default:
      return 3
  }
}

/**
 * Returns the effective levels object for a plant.
 * Uses plant.levels if present, otherwise derives from text fields.
 */
export function effectiveLevels(plant) {
  if (plant?.levels) return plant.levels
  return {
    water:      textToLevel(plant?.watering, 'water'),
    light:      textToLevel(plant?.light, 'light'),
    temp:       textToLevel(plant?.temperature, 'temp'),
    humidity:   textToLevel(plant?.humidity, 'humidity'),
    fertilizer: textToLevel(plant?.fertilization, 'fertilizer'),
  }
}

/**
 * Derives up to 3 condition tags from a levels object.
 * Mirrors the deriveConditionTags() function from the DA mockup.
 */
export function deriveConditionTags(levels) {
  if (!levels) return []
  const tags = []

  if (levels.light >= 5)      tags.push({ icon: 'sun', label: 'Plein soleil' })
  else if (levels.light >= 4) tags.push({ icon: 'sun', label: 'Forte lumière' })
  else if (levels.light <= 2) tags.push({ icon: 'sun', label: 'Mi-ombre' })

  if (levels.water <= 1)      tags.push({ icon: 'water', label: 'Très peu d\'eau' })
  else if (levels.water <= 2) tags.push({ icon: 'water', label: 'Peu d\'eau' })
  else if (levels.water >= 5) tags.push({ icon: 'water', label: 'Beaucoup d\'eau' })

  if (levels.humidity >= 5)   tags.push({ icon: 'humidity', label: 'Très humide' })
  else if (levels.humidity <= 1) tags.push({ icon: 'humidity', label: 'Air sec' })

  if (levels.temp >= 4)       tags.push({ icon: 'temp', label: 'Chaud' })
  else if (levels.temp <= 2)  tags.push({ icon: 'temp', label: 'Frais ok' })

  return tags.slice(0, 3)
}
