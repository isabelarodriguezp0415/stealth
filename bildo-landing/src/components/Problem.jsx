import React from 'react';
import { Clock, FileText, AlertTriangle, TrendingDown } from 'lucide-react';

const Problem = () => {
  const problems = [
    {
      icon: Clock,
      title: 'Análisis Manual y Lento',
      description: 'Días o semanas interpretando decretos y normativas urbanas complejas.',
    },
    {
      icon: FileText,
      title: 'Datos Dispersos',
      description: 'Información catastral y normativa fragmentada en múltiples fuentes.',
    },
    {
      icon: AlertTriangle,
      title: 'Alto Riesgo de Error',
      description: 'Interpretaciones subjetivas que pueden llevar a decisiones costosas.',
    },
    {
      icon: TrendingDown,
      title: 'Oportunidades Perdidas',
      description: 'Lotes con potencial que no se identifican por falta de análisis sistemático.',
    },
  ];

  return (
    <section className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-primary mb-4">
            El Desafío del Mercado Inmobiliario
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Identificar oportunidades de desarrollo sigue siendo un proceso complejo,
            manual y dependiente de la interpretación individual.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {problems.map((problem, index) => {
            const Icon = problem.icon;
            return (
              <div
                key={index}
                className="bg-white rounded-xl p-6 shadow-lg hover:shadow-xl transition-shadow"
              >
                <div className="bg-accent/10 rounded-lg w-14 h-14 flex items-center justify-center mb-4">
                  <Icon className="text-accent" size={28} />
                </div>
                <h3 className="text-xl font-bold text-primary mb-3">
                  {problem.title}
                </h3>
                <p className="text-gray-600">
                  {problem.description}
                </p>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default Problem;
