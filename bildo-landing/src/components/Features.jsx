import React from 'react';
import {
  Database,
  FileSearch,
  Calculator,
  MapPin,
  BarChart3,
  Shield,
  Layers,
  Download
} from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: FileSearch,
      title: 'Interpretación Normativa',
      description: 'IA lee y comprende decretos, POTs y normativas urbanas automáticamente.',
      color: 'accent',
    },
    {
      icon: Calculator,
      title: 'Cálculo de Edificabilidad',
      description: 'Determina el máximo aprovechamiento permitido según la normativa vigente.',
      color: 'secondary',
    },
    {
      icon: Database,
      title: 'Integración Catastral',
      description: 'Conexión directa con bases de datos catastrales y geográficas.',
      color: 'accent',
    },
    {
      icon: MapPin,
      title: 'Geolocalización Precisa',
      description: 'Visualización de lotes y oportunidades en mapas interactivos.',
      color: 'secondary',
    },
    {
      icon: BarChart3,
      title: 'Análisis de Potencial',
      description: 'Priorización automática de oportunidades según criterios personalizables.',
      color: 'accent',
    },
    {
      icon: Shield,
      title: 'Validación Técnica',
      description: 'Resultados verificados y respaldados por fuentes oficiales.',
      color: 'secondary',
    },
    {
      icon: Layers,
      title: 'Análisis Multi-Lote',
      description: 'Procesa y compara múltiples predios simultáneamente.',
      color: 'accent',
    },
    {
      icon: Download,
      title: 'Reportes Exportables',
      description: 'Genera informes técnicos en PDF listos para presentar.',
      color: 'secondary',
    },
  ];

  return (
    <section id="caracteristicas" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-primary mb-4">
            Características Potentes
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Todo lo que necesitas para identificar, analizar y priorizar oportunidades
            inmobiliarias en una sola plataforma.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            const colorClass = feature.color === 'accent'
              ? 'bg-accent/10 text-accent'
              : 'bg-secondary/10 text-secondary';

            return (
              <div
                key={index}
                className="group hover:bg-gray-50 rounded-xl p-6 transition-all hover:shadow-lg"
              >
                <div className={`${colorClass} rounded-lg w-14 h-14 flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <Icon size={28} />
                </div>
                <h3 className="text-lg font-bold text-primary mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-600 text-sm">
                  {feature.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Features;
