import React from 'react';
import { Upload, Cpu, LineChart, CheckCircle } from 'lucide-react';

const HowItWorks = () => {
  const steps = [
    {
      number: '01',
      icon: Upload,
      title: 'Ingresa el Lote',
      description: 'Proporciona la dirección, coordenadas o datos catastrales del predio que deseas analizar.',
    },
    {
      number: '02',
      icon: Cpu,
      title: 'IA Analiza',
      description: 'Nuestra IA procesa la normativa urbana, calcula parámetros y evalúa restricciones en segundos.',
    },
    {
      number: '03',
      icon: LineChart,
      title: 'Visualiza Resultados',
      description: 'Obtén edificabilidad, altura máxima, uso de suelo y potencial de desarrollo con gráficos claros.',
    },
    {
      number: '04',
      icon: CheckCircle,
      title: 'Toma Decisiones',
      description: 'Exporta reportes técnicos y toma decisiones informadas basadas en datos precisos.',
    },
  ];

  return (
    <section id="como-funciona" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold text-primary mb-4">
            Cómo Funciona BILDO
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            De la complejidad normativa a decisiones estratégicas en 4 pasos simples.
          </p>
        </div>

        <div className="relative">
          {/* Connection Line - Desktop */}
          <div className="hidden lg:block absolute top-1/2 left-0 right-0 h-1 bg-gradient-to-r from-accent via-secondary to-accent transform -translate-y-1/2 opacity-20"></div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
            {steps.map((step, index) => {
              const Icon = step.icon;
              return (
                <div
                  key={index}
                  className="relative bg-white rounded-xl p-8 shadow-lg hover:shadow-xl transition-all group"
                >
                  {/* Step Number */}
                  <div className="absolute -top-4 -left-4 bg-gradient-accent text-white w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg shadow-lg">
                    {step.number}
                  </div>

                  <div className="mt-4">
                    <div className="bg-primary/10 rounded-lg w-16 h-16 flex items-center justify-center mb-6 group-hover:bg-accent/10 transition-colors">
                      <Icon className="text-primary group-hover:text-accent transition-colors" size={32} />
                    </div>

                    <h3 className="text-xl font-bold text-primary mb-3">
                      {step.title}
                    </h3>

                    <p className="text-gray-600">
                      {step.description}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Additional Info */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center bg-accent/10 text-accent px-6 py-3 rounded-full font-semibold">
            <Cpu className="mr-2" size={20} />
            Todo el proceso toma menos de 10 segundos
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
