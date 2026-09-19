import { motion } from "framer-motion";
import { ReactNode } from "react";
import { ArrowRight } from "lucide-react";

/**
 * 链表节点接口
 */
export interface LinkedListNode {
  val: number | string;
  next: number | null; // 指向下一个节点的索引，null 表示链表结束
}

/**
 * 指针状态
 */
export interface PointerState {
  name: string;
  index: number | null;
  color: string;
  label?: string;
}

/**
 * 链表节点状态
 */
export interface LinkedListNodeState {
  index: number;
  isActive?: boolean; // 是否有指针指向此节点
  activePointers?: string[]; // 哪些指针指向此节点
  isReversed?: boolean; // 指针是否已反转（用于反转链表）
  customState?: Record<string, any>;
}

/**
 * LinkedListTemplate 属性
 */
export interface LinkedListTemplateProps {
  // 数据
  nodes: LinkedListNode[];
  
  // 指针配置
  pointers?: PointerState[];
  
  // 核心渲染函数（完全自定义节点渲染）
  renderNode: (node: LinkedListNode, index: number, state: LinkedListNodeState) => ReactNode;
  
  // 可选的自定义渲染
  renderContainer?: (children: ReactNode[]) => ReactNode;
  renderHeader?: () => ReactNode;
  renderFooter?: () => ReactNode;
  renderLegend?: (pointers: PointerState[]) => ReactNode;
  
  // 状态计算函数
  getNodeState?: (index: number, node: LinkedListNode) => Partial<LinkedListNodeState>;
  
  // 箭头渲染（可选，默认使用 ArrowRight）
  renderArrow?: (fromIndex: number, toIndex: number | null, isReversed: boolean) => ReactNode;
  
  // 动画配置
  animation?: {
    node?: any;
    arrow?: any;
    duration?: number;
  };
  
  // 布局配置
  layout?: {
    direction?: 'horizontal' | 'vertical';
    gap?: string;
    nodeGap?: string; // 节点之间的间距
  };
  
  // 样式
  className?: string;
  
  // 空链表显示
  emptyMessage?: string;
}

/**
 * 默认箭头渲染
 */
function DefaultArrow({ 
  isReversed 
}: { 
  isReversed: boolean;
}) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      className={`flex flex-col items-center justify-center gap-1 mx-2 ${
        isReversed ? 'text-green-500' : 'text-gray-400'
      }`}
    >
      <motion.div
        initial={{ x: isReversed ? 5 : -5 }}
        animate={{ x: 0 }}
        transition={{ duration: 0.5, repeat: Infinity, repeatType: "reverse" }}
      >
        <ArrowRight 
          size={32} 
          strokeWidth={2.5}
          className="drop-shadow-sm"
        />
      </motion.div>
    </motion.div>
  );
}

/**
 * 默认图例渲染
 */
function DefaultLegend({ pointers }: { pointers: PointerState[] }) {
  if (pointers.length === 0) return null;
  
  return (
    <div className="flex gap-4 items-center justify-center flex-wrap mt-6">
      {pointers.map((pointer) => (
        <div
          key={pointer.name}
          className="flex items-center gap-2 bg-gradient-to-r from-gray-50 to-gray-100 px-4 py-2 rounded-xl border border-gray-200 shadow-sm"
        >
          <div
            className="w-6 h-6 rounded-lg shadow-md"
            style={{ backgroundColor: pointer.color }}
          />
          <span className="text-gray-700 font-semibold text-sm">
            {pointer.label || pointer.name.toUpperCase()} 指针
          </span>
        </div>
      ))}
    </div>
  );
}

/**
 * 通用链表可视化模板
 * 
 * 特点：
 * 1. 提供统一的链表布局和节点连接
 * 2. 支持多个指针可视化
 * 3. 完全保留视觉定制能力（通过 renderNode）
 * 4. 支持指针反转状态（用于反转链表）
 */
export function LinkedListTemplate({
  nodes,
  pointers = [],
  renderNode,
  renderContainer,
  renderHeader,
  renderFooter,
  renderLegend,
  getNodeState,
  renderArrow,
  animation,
  layout = {},
  className = '',
  emptyMessage = '空链表',
}: LinkedListTemplateProps) {
  const {
    direction = 'horizontal',
    gap = '0.5rem',
    nodeGap = '0.75rem',
  } = layout;

  // 空链表处理
  if (nodes.length === 0) {
    return (
      <div className={`flex items-center justify-center h-32 text-gray-500 bg-white rounded-lg shadow-sm border border-gray-200 p-6 ${className}`}>
        {emptyMessage}
      </div>
    );
  }

  // 计算每个节点的状态
  const getNodeStateInternal = (index: number, node: LinkedListNode): LinkedListNodeState => {
    const activePointers = pointers
      .filter(p => p.index === index)
      .map(p => p.name);
    
    const baseState: LinkedListNodeState = {
      index,
      isActive: activePointers.length > 0,
      activePointers,
      isReversed: node.next !== null && node.next < index, // 反转判断：next 指向更小的索引
      ...getNodeState?.(index, node),
    };
    
    return baseState;
  };

  // 渲染节点和箭头
  const renderNodes = () => {
    return nodes.map((node, index) => {
      const state = getNodeStateInternal(index, node);
      const hasNext = node.next !== null;
      const isReversed = state.isReversed || false;

      return (
        <div key={index} className="flex items-center" style={{ gap: nodeGap }}>
          {/* 节点 */}
          <motion.div
            variants={animation?.node}
            initial="hidden"
            animate="visible"
            exit="exit"
            transition={{ duration: animation?.duration || 0.3 }}
          >
            {renderNode(node, index, state)}
          </motion.div>

          {/* 箭头 */}
          {hasNext && (
            <motion.div
              variants={animation?.arrow}
              initial="hidden"
              animate="visible"
              transition={{ duration: animation?.duration || 0.3 }}
            >
              {renderArrow ? (
                renderArrow(index, node.next, isReversed)
              ) : (
                <DefaultArrow isReversed={isReversed} />
              )}
            </motion.div>
          )}
        </div>
      );
    });
  };

  const nodeElements = renderNodes();

  // 容器样式
  const containerClass = `flex ${
    direction === 'horizontal' ? 'flex-row' : 'flex-col'
  } items-center ${direction === 'horizontal' ? 'flex-wrap' : ''} ${className}`;

  return (
    <div className="w-full">
      {/* 头部插槽 */}
      {renderHeader?.()}
      
      {/* 链表容器 */}
      <div className="bg-gradient-to-b from-slate-50 via-gray-50 to-white p-8 rounded-xl border border-gray-200 w-full shadow-inner">
        <motion.div
          className={containerClass}
          style={{ gap }}
          initial="hidden"
          animate="visible"
        >
          {renderContainer ? renderContainer(nodeElements) : nodeElements}
        </motion.div>
      </div>

      {/* 图例 */}
      {renderLegend ? (
        renderLegend(pointers)
      ) : (
        <DefaultLegend pointers={pointers} />
      )}
      
      {/* 底部插槽 */}
      {renderFooter?.()}
    </div>
  );
}

