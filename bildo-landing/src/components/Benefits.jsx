import React from 'react';
import { TrendingUp, Clock, DollarSign, Users, Target, Award } from 'lucide-react';

const Benefits = () => {
  const benefits = [
    {
      icon: Clock,
      metric: '90%',
      title: 'Reducción de Tiempo',
      description: 'De semanas a segundos en análisis normativo.',
      gradient: 'from-accent to-accent-light',
    },
    {
      icon: DollarSign,
      metric: '+35%',
      title: 'Mejor ROI',
      description: 'Identifica oportunidades de mayor rentabilidad.',
      gradient: 'from-secondary to-secondary-light',
    },
    {
      icon: Target,
      metric: '99%',
      title: 'Precisión',
      description: 'Cálculos exactos basados en normativa oficial.',
      gradient: 'from-accent to-accent-light',
    },
    {
      icon: TrendingUp,
      metric: '5x',
      title: 'Más Análisis',
      description: 'Evalúa 5 veces más lotes en el mismo tiempo.',
      gradient: 'from-secondary to-secondary-light',
    },
    {
      icon: Users,
      metric: '100%',
      title: 'Equipo Alineado',
      description: 'Una sola fuente de verdad para todos.',
      gradient: 'from-accent to-accent-light',
    },
    {
      icon: Award,
      metric: 'Pro',
      title: 'Ventaja Competitiva',
      description: 'Identifica oportunidades antes que la competencia.',
      gradient: 'from-secondary to-secondary-light',
    },
  ];

  return (
    <section id="beneficios" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-primary mb-4">
            Beneficios Cuantificables
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            BILDO transforma la forma en que constructoras e inversionistas identifican
            y evalúan oportunidades inmobiliarias.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {benefits.map((benefit, index) => {
            const Icon = benefit.icon;
            return (
              <div
                key={index}
                className="relative group"
              >
                <div className="bg-white border-2 border-gray-100 rounded-xl p-8 hover:border-transparent hover:shadow-2xl transition-all h-full">
                  {/* Gradient Border on Hover */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${benefit.gradient} rounded-xl opacity-0 group-hover:opacity-100 transition-opacity -z-10`}></div>

                  <div className={`bg-gradient-to-br ${benefit.gradient} rounded-lg w-14 h-14 flex items-center justify-center mb-6`}>
                    <Icon className="text-white" size={28} />
                  </div>

                  <div className={`text-5xl font-bold bg-gradient-to-br ${benefit.gradient} bg-clip-text text-transparent mb-2`}>
                    {benefit.metric}
                  </div>

                  <h3 className="text-xl font-bold text-primary mb-3">
                    {benefit.title}
                  </h3>

                  <p className="text-gray-600">
                    {benefit.description}
                  </p>
                </div>
              </div>
            );
          })}
        </div>

        {/* Testimonial / Social Proof */}
        <div className="mt-20 bg-gradient-to-br from-primary to-secondary rounded-2xl p-12 text-white">
          <div className="max-w-4xl mx-auto">
            <div className="text-center">
              <div className="text-6xl mb-4">"</div>
              <p className="text-2xl mb-8 italic">
                BILDO nos permitió analizar 200 lotes en una semana, algo que antes nos tomaba meses.
                La precisión del análisis normativo es impresionante y nos ha ayudado a identificar
                oportunidades que hubiéramos pasado por alto.
              </p>
              <div className="flex items-center justify-center space-x-4">
                <div className="w-12 h-12 bg-accent rounded-full flex items-center justify-center font-bold text-xl">
                  JM
                </div>
                <div className="text-left">
                  <div className="font-bold">Juan Martínez</div>
                  <div className="text-gray-300 text-sm">Director de Desarrollo - Constructora XYZ</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Benefits;
