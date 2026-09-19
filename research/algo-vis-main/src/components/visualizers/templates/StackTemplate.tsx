import { motion, AnimatePresence } from "framer-motion";
import { ReactNode } from "react";
import { ArrowDown, ArrowUp } from "lucide-react";

/**
 * 栈元素状态
 */
export interface StackItemState {
  index: number;
  isTop?: boolean; // 是否为栈顶元素
  isActive?: boolean; // 是否正在操作（push/pop）
  action?: 'push' | 'pop' | null; // 当前操作类型
  customState?: Record<string, any>;
}

/**
 * StackTemplate 属性
 */
export interface StackTemplateProps<T = any> {
  // 数据（栈底到栈顶的顺序）
  data: T[];
  
  // 核心渲染函数（完全自定义元素渲染）
  renderItem: (item: T, index: number, state: StackItemState) => ReactNode;
  
  // 可选的自定义渲染
  renderContainer?: (children: ReactNode[]) => ReactNode;
  renderHeader?: () => ReactNode;
  renderFooter?: () => ReactNode;
  renderEmpty?: () => ReactNode;
  
  // 状态计算函数
  getItemState?: (index: number, item: T) => Partial<StackItemState>;
  
  // 动画配置
  animation?: {
    item?: any;
    duration?: number;
  };
  
  // 布局配置
  layout?: {
    direction?: 'vertical' | 'horizontal'; // 栈的方向（通常为 vertical）
    gap?: string; // 元素之间的间距
    maxWidth?: string; // 最大宽度
    minHeight?: string; // 最小高度
  };
  
  // 样式
  className?: string;
  
  // 空栈消息
  emptyMessage?: string;
  
  // 显示栈底标记
  showBottomMarker?: boolean;
  
  // 显示栈大小
  showSize?: boolean;
  
  // 当前操作（用于显示动画）
  currentAction?: 'push' | 'pop' | null;
}

/**
 * 默认空栈渲染
 */
function DefaultEmpty({ message }: { message: string }) {
  return (
    <div className="absolute inset-0 flex items-center justify-center">
      <div className="text-center text-gray-400">
        <div className="text-6xl mb-2">📭</div>
        <p className="text-sm">{message}</p>
      </div>
    </div>
  );
}

/**
 * 通用栈可视化模板
 * 
 * 特点：
 * 1. 提供统一的栈布局（垂直堆叠，LIFO）
 * 2. 支持 push/pop 动画
 * 3. 完全保留视觉定制能力（通过 renderItem）
 * 4. 自动处理栈顶/栈底标记
 */
export function StackTemplate<T = any>({
  data,
  renderItem,
  renderContainer,
  renderHeader,
  renderFooter,
  renderEmpty,
  getItemState,
  animation,
  layout = {},
  className = '',
  emptyMessage = '栈为空',
  showBottomMarker = true,
  showSize = false,
  currentAction = null,
}: StackTemplateProps<T>) {
  const {
    direction = 'vertical',
    gap = '0.5rem',
    maxWidth = '200px',
    minHeight = '350px',
  } = layout;

  // 计算每个元素的状态（栈底到栈顶，索引从 0 开始）
  const getItemStateInternal = (index: number, item: T): StackItemState => {
    const stackIndex = data.length - 1 - index; // 转换为栈中的位置（0 = 栈底）
    const isTop = stackIndex === data.length - 1;
    
    const baseState: StackItemState = {
      index: stackIndex,
      isTop,
      isActive: isTop && currentAction !== null,
      action: isTop ? currentAction : null,
      ...getItemState?.(index, item),
    };
    
    return baseState;
  };

  // 渲染栈元素（从栈底到栈顶）
  const renderItems = () => {
    // 反转数组，使栈底在底部，栈顶在顶部
    const reversedData = [...data].reverse();
    
    return reversedData.map((item, displayIndex) => {
      const state = getItemStateInternal(displayIndex, item);
      
      return (
        <motion.div
          key={`${displayIndex}-${data.length}`}
          variants={animation?.item}
          initial="hidden"
          animate="visible"
          exit="exit"
          transition={{ duration: animation?.duration || 0.3 }}
          className={state.isTop ? "z-10" : ""}
        >
          {renderItem(item, state.index, state)}
        </motion.div>
      );
    });
  };

  const items = renderItems();

  // 容器样式
  const containerClass = `relative min-h-[${minHeight}] bg-gradient-to-b from-purple-50 to-white p-6 rounded-lg border border-purple-100 flex ${
    direction === 'vertical' ? 'flex-col-reverse' : 'flex-row-reverse'
  } items-center ${className}`;

  return (
    <div className="w-full">
      {/* 头部插槽（可以显示栈大小、操作提示等） */}
      {renderHeader?.()}
      
      {/* 栈容器 */}
      <div className={containerClass} style={{ maxWidth }}>
        {data.length === 0 ? (
          renderEmpty ? (
            renderEmpty()
          ) : (
            <DefaultEmpty message={emptyMessage} />
          )
        ) : (
          <div
            className={`flex ${
              direction === 'vertical' ? 'flex-col-reverse' : 'flex-row-reverse'
            } gap-2 w-full`}
            style={{ gap }}
          >
            <AnimatePresence>
              {renderContainer ? renderContainer(items) : items}
            </AnimatePresence>
          </div>
        )}

        {/* 栈底标记 */}
        {showBottomMarker && data.length > 0 && (
          <div className={`mt-4 w-full border-t-4 border-dashed border-gray-300 pt-2 text-center ${
            direction === 'vertical' ? '' : 'border-l-4 border-t-0 pt-0 pl-2'
          }`}>
            <span className="text-xs font-semibold text-gray-500">栈底</span>
          </div>
        )}
      </div>

      {/* 操作动画提示 */}
      {currentAction && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="flex items-center justify-center mt-2"
        >
          {currentAction === 'push' ? (
            <ArrowDown className="text-blue-500 animate-bounce" size={24} />
          ) : (
            <ArrowUp className="text-red-500 animate-bounce" size={24} />
          )}
        </motion.div>
      )}

      {/* 栈大小显示 */}
      {showSize && (
        <div className="mt-2 text-center">
          <span className="text-sm bg-purple-100 text-purple-700 px-3 py-1 rounded-full font-semibold">
            大小: {data.length}
          </span>
        </div>
      )}
      
      {/* 底部插槽 */}
      {renderFooter?.()}
    </div>
  );
}

