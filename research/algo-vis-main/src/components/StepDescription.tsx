import { Info } from "lucide-react";

interface StepDescriptionProps {
  description: string;
  variables?: Record<string, unknown>;
}

function StepDescription({ description, variables }: StepDescriptionProps) {
  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
      <div className="flex items-start gap-3">
        <Info className="text-blue-500 flex-shrink-0 mt-0.5" size={20} />
        <div className="flex-1">
          <p className="text-gray-800 mb-2">{description}</p>
          {variables && Object.keys(variables).length > 0 && (
            <div className="mt-3 bg-white rounded p-3 border border-blue-100">
              <p className="text-sm font-semibold text-gray-700 mb-2">
                当前变量：
              </p>
              <div className="grid grid-cols-2 gap-2">
                {Object.entries(variables).map(([key, value]) => (
                  <div key={key} className="text-sm">
                    <span className="font-mono text-blue-600">{key}</span>
                    <span className="text-gray-500"> = </span>
                    <span className="font-mono text-gray-800">
                      {JSON.stringify(value)}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default StepDescription;

