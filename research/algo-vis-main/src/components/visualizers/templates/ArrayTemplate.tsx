import { motion, Variants } from "framer-motion";
import { ReactNode } from "react";

/**
 * 数组元素状态
 */
export interface ArrayItemState {
  index: number;
  isActive?: boolean;
  isHighlighted?: boolean;
  isDisabled?: boolean;
  customState?: Record<string, any>;
}

/**
 * ArrayTemplate 属性
 */
export interface ArrayTemplateProps<T = any> {
  // 数据
  data: T[];
  
  // 核心渲染函数（完全自定义）
  renderItem: (item: T, index: number, state: ArrayItemState) => ReactNode;
  
  // 可选的自定义渲染
  renderContainer?: (children: ReactNode[]) => ReactNode;
  renderHeader?: () => ReactNode;
  renderFooter?: () => ReactNode;
  renderBackground?: () => ReactNode;
  
  // 状态计算函数（用于确定每个元素的状态）
  getItemState?: (index: number) => Partial<ArrayItemState>;
  
  // 动画配置
  animation?: {
    container?: Variants;
    item?: Variants;
    duration?: number;
  };
  
  // 布局配置
  layout?: {
    gap?: string;
    direction?: 'row' | 'column';
    align?: 'start' | 'center' | 'end';
    justify?: 'start' | 'center' | 'end' | 'between' | 'around';
    wrap?: boolean;
  };
  
  // 交互
  onItemClick?: (index: number, item: T) => void;
  
  // 样式
  className?: string;
}

/**
 * 通用数组可视化模板
 * 
 * 特点：
 * 1. 提供统一的数组布局和动画框架
 * 2. 完全保留视觉定制能力（通过 renderItem）
 * 3. 支持插槽式扩展（header/footer/background）
 */
export function ArrayTemplate<T = any>({
  data,
  renderItem,
  renderContainer,
  renderHeader,
  renderFooter,
  renderBackground,
  getItemState,
  animation,
  layout = {},
  onItemClick,
  className = '',
}: ArrayTemplateProps<T>) {
  const {
    gap = '0.5rem',
    direction = 'row',
    align = 'center',
    justify = 'center',
    wrap = true,
  } = layout;

  // 默认容器样式
  const containerClass = `flex ${
    direction === 'row' ? 'flex-row' : 'flex-col'
  } ${
    align === 'start' ? 'items-start' : align === 'end' ? 'items-end' : 'items-center'
  } ${
    justify === 'start' ? 'justify-start' :
    justify === 'end' ? 'justify-end' :
    justify === 'between' ? 'justify-between' :
    justify === 'around' ? 'justify-around' :
    'justify-center'
  } ${wrap ? 'flex-wrap' : ''} ${className}`;

  // 渲染元素列表
  const renderItems = () => {
    return data.map((item, index) => {
      const baseState: ArrayItemState = {
        index,
        ...getItemState?.(index),
      };

      return (
        <motion.div
          key={index}
          variants={animation?.item}
          initial="hidden"
          animate="visible"
          exit="exit"
          transition={{ duration: animation?.duration || 0.3 }}
          onClick={() => onItemClick?.(index, item)}
          style={{ cursor: onItemClick ? 'pointer' : 'default' }}
        >
          {renderItem(item, index, baseState)}
        </motion.div>
      );
    });
  };

  const items = renderItems();

  return (
    <div className="w-full">
      {/* 背景层 */}
      {renderBackground?.()}
      
      {/* 头部插槽 */}
      {renderHeader?.()}
      
      {/* 数组容器 */}
      <motion.div
        className={containerClass}
        style={{ gap }}
        variants={animation?.container}
        initial="hidden"
        animate="visible"
      >
        {renderContainer ? renderContainer(items) : items}
      </motion.div>
      
      {/* 底部插槽 */}
      {renderFooter?.()}
    </div>
  );
}
