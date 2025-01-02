import { Scene, Light, Camera, WebGLRenderer, WebGLRendererParameters, Renderer } from 'three';
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js';
import { ThreeForceGraphGeneric, NodeObject, LinkObject } from 'three-forcegraph';

export interface ConfigOptions {
  controlType?: 'trackball' | 'orbit' | 'fly'
  rendererConfig?: WebGLRendererParameters,
  extraRenderers?: Renderer[]
}

type Accessor<In, Out> = Out | string | ((obj: In) => Out);
type ObjAccessor<T, InT = object> = Accessor<InT, T>;

type Coords = { x: number; y: number; z: number; };

// don't surface these internal props from inner ThreeForceGraph
type ExcludedInnerProps = 'onLoading' | 'onFinishLoading' | 'onUpdate' | 'onFinishUpdate' | 'tickFrame' | 'd3AlphaTarget' | 'resetCountdown';

export interface ForceGraph3DGenericInstance<ChainableInstance, N extends NodeObject = NodeObject, L extends LinkObject<N> = LinkObject<N>>
    extends Omit<ThreeForceGraphGeneric<ChainableInstance, N, L>, ExcludedInnerProps> {
  (element: HTMLElement): ChainableInstance;
  _destructor(): void;

  // Container layout
  width(): number;
  width(width: number): ChainableInstance;
  height(): number;
  height(height: number): ChainableInstance;
  backgroundColor(): string;
  backgroundColor(color: string): ChainableInstance;
  showNavInfo(): boolean;
  showNavInfo(enabled: boolean): ChainableInstance;

  // Labels
  nodeLabel(): ObjAccessor<string, N>;
  nodeLabel(textAccessor: ObjAccessor<string, N>): ChainableInstance;
  linkLabel(): ObjAccessor<string, L>;
  linkLabel(textAccessor: ObjAccessor<string, L>): ChainableInstance;

  // Interaction
  onNodeClick(callback: (node: N, event: MouseEvent) => void): ChainableInstance;
  onNodeRightClick(callback: (node: N, event: MouseEvent) => void): ChainableInstance;
  onNodeHover(callback: (node: N | null, previousNode: N | null) => void): ChainableInstance;
  onNodeDrag(callback: (node: N, translate: Coords) => void): ChainableInstance;
  onNodeDragEnd(callback: (node: N, translate: Coords) => void): ChainableInstance;
  onLinkClick(callback: (link: L, event: MouseEvent) => void): ChainableInstance;
  onLinkRightClick(callback: (link: L, event: MouseEvent) => void): ChainableInstance;
  onLinkHover(callback: (link: L | null, previousLink: L | null) => void): ChainableInstance;
  onBackgroundClick(callback: (event: MouseEvent) => void): ChainableInstance;
  onBackgroundRightClick(callback: (event: MouseEvent) => void): ChainableInstance;
  linkHoverPrecision(): number;
  linkHoverPrecision(precision: number): ChainableInstance;
  enablePointerInteraction(): boolean;
  enablePointerInteraction(enable: boolean): ChainableInstance;
  enableNodeDrag(): boolean;
  enableNodeDrag(enable: boolean): ChainableInstance;
  enableNavigationControls(): boolean;
  enableNavigationControls(enable: boolean): ChainableInstance;

  // Render control
  pauseAnimation(): ChainableInstance;
  resumeAnimation(): ChainableInstance;
  cameraPosition(): Coords;
  cameraPosition(position: Partial<Coords>, lookAt?: Coords, transitionMs?: number): ChainableInstance;
  zoomToFit(durationMs?: number, padding?: number, nodeFilter?: (node: N) => boolean): ChainableInstance;
  postProcessingComposer(): EffectComposer;
  lights(): Light[];
  lights(lights: Light[]): ChainableInstance;
  scene(): Scene;
  camera(): Camera;
  renderer(): WebGLRenderer;
  controls(): object;

  // Utility
  graph2ScreenCoords(x: number, y: number, z: number): Coords;
  screen2GraphCoords(screenX: number, screenY: number, distance: number): Coords;
}

export type ForceGraph3DInstance<NodeType = NodeObject, LinkType = LinkObject<NodeType>> = ForceGraph3DGenericInstance<ForceGraph3DInstance<NodeType, LinkType>, NodeType, LinkType>;

declare function ForceGraph3D<NodeType = NodeObject, LinkType = LinkObject<NodeType>>(configOptions?: ConfigOptions): ForceGraph3DInstance<NodeType, LinkType>;

export default ForceGraph3D;