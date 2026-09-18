import { motion } from "framer-motion";

interface ArrayVisualizerProps {
  array: number[];
  highlightedIndices?: number[];
  currentIndex?: number;
  targetIndex?: number;
  title?: string;
}

function ArrayVisualizer({
  array,
  highlightedIndices = [],
  currentIndex,
  targetIndex,
  title = "数组可视化",
}: ArrayVisualizerProps) {
  const getBarColor = (index: number): string => {
    if (targetIndex !== undefined && index === targetIndex) {
      return "bg-green-500";
    }
    if (currentIndex !== undefined && index === currentIndex) {
      return "bg-yellow-500";
    }
    if (highlightedIndices.includes(index)) {
      return "bg-blue-500";
    }
    return "bg-gray-400";
  };

  const getTextColor = (index: number): string => {
    if (targetIndex !== undefined && index === targetIndex) {
      return "text-green-600";
    }
    if (currentIndex !== undefined && index === currentIndex) {
      return "text-yellow-600";
    }
    if (highlightedIndices.includes(index)) {
      return "text-blue-600";
    }
    return "text-gray-600";
  };

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold mb-4 text-gray-700">{title}</h3>
      <div className="flex items-end justify-center gap-2 min-h-[200px] bg-white p-6 rounded-lg shadow-sm border border-gray-200">
        {array.map((value, index) => (
          <motion.div
            key={index}
            className="flex flex-col items-center gap-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.05 }}
          >
            {/* 值显示 */}
            <motion.div
              className={`text-sm font-bold ${getTextColor(index)}`}
              animate={{
                scale: currentIndex === index || targetIndex === index ? 1.2 : 1,
              }}
            >
              {value}
            </motion.div>

            {/* 柱状图 */}
            <motion.div
              className={`w-12 ${getBarColor(index)} rounded-t-md transition-colors duration-300 flex items-end justify-center pb-2`}
              style={{ height: `${Math.max(40, Math.abs(value) * 4)}px` }}
              animate={{
                scale: currentIndex === index || targetIndex === index ? 1.1 : 1,
              }}
              whileHover={{ scale: 1.05 }}
            >
              <span className="text-white text-xs font-semibold">{value}</span>
            </motion.div>

            {/* 索引 */}
            <div className={`text-xs font-medium ${getTextColor(index)}`}>
              [{index}]
            </div>
          </motion.div>
        ))}
      </div>

      {/* 图例 */}
      <div className="flex items-center justify-center gap-6 mt-4 text-sm">
        {currentIndex !== undefined && (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-yellow-500 rounded"></div>
            <span>当前遍历</span>
          </div>
        )}
        {targetIndex !== undefined && (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-green-500 rounded"></div>
            <span>找到目标</span>
          </div>
        )}
        {highlightedIndices.length > 0 && (
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 bg-blue-500 rounded"></div>
            <span>已检查</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default ArrayVisualizer;

