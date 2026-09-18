import { ReactNode } from "react";
import { ArrayTemplate, ArrayItemState } from "./ArrayTemplate";

/**
 * 字符串元素状态（扩展 ArrayItemState）
 */
export interface StringItemState extends ArrayItemState {
  isCurrent?: boolean; // 当前遍历位置
  isPassed?: boolean; // 已遍历过
  isMatched?: boolean; // 已匹配
  char?: string; // 字符值
}

/**
 * StringTemplate 属性
 */
export interface StringTemplateProps {
  // 数据
  data: string | string[];
  
  // 核心渲染函数（完全自定义字符渲染）
  renderChar: (char: string, index: number, state: StringItemState) => ReactNode;
  
  // 可选的自定义渲染
  renderContainer?: (children: ReactNode[]) => ReactNode;
  renderHeader?: () => ReactNode;
  renderFooter?: () => ReactNode;
  renderBackground?: () => ReactNode;
  
  // 状态计算函数
  getCharState?: (index: number) => Partial<StringItemState>;
  
  // 当前遍历位置
  currentIndex?: number;
  
  // 动画配置
  animation?: {
    container?: any;
    item?: any;
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
  onCharClick?: (index: number, char: string) => void;
  
  // 样式
  className?: string;
  
  // 字符颜色映射（可选）
  getCharColor?: (char: string) => string;
}

/**
 * 通用字符串可视化模板
 * 
 * 特点：
 * 1. 基于 ArrayTemplate，针对字符串优化
 * 2. 支持字符遍历状态（current/passed/matched）
 * 3. 完全保留视觉定制能力（通过 renderChar）
 * 4. 支持字符颜色映射
 */
export function StringTemplate({
  data,
  renderChar,
  renderContainer,
  renderHeader,
  renderFooter,
  renderBackground,
  getCharState,
  currentIndex,
  animation,
  layout = {},
  onCharClick,
  className = '',
}: StringTemplateProps) {
  // 转换为字符数组
  const chars = typeof data === 'string' ? data.split('') : data;
  
  // 合并状态计算函数
  const getItemState = (index: number): Partial<StringItemState> => {
    const isCurrent = currentIndex === index;
    const isPassed = currentIndex !== undefined && index < currentIndex;
    
    const baseState: Partial<StringItemState> = {
      index,
      isCurrent,
      isPassed,
      char: chars[index],
      ...getCharState?.(index),
    };
    
    return baseState;
  };
  
  // 包装 renderChar 为 renderItem
  const renderItem = (char: string, index: number, state: ArrayItemState) => {
    const stringState: StringItemState = {
      ...state,
      char,
      isCurrent: currentIndex === index,
      isPassed: currentIndex !== undefined && index < currentIndex,
    };
    
    return renderChar(char, index, stringState);
  };
  
  // 使用 ArrayTemplate
  return (
    <ArrayTemplate
      data={chars}
      renderItem={renderItem}
      renderContainer={renderContainer}
      renderHeader={renderHeader}
      renderFooter={renderFooter}
      renderBackground={renderBackground}
      getItemState={getItemState}
      animation={animation}
      layout={layout}
      onItemClick={onCharClick}
      className={className}
    />
  );
}

