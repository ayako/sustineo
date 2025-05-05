import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { immer } from 'zustand/middleware/immer'

export interface TextData {
  // this would be the callId
  id: string;
  type: "text";
  value: string;
  annotations: {
    type: string;
    text: string;
    start_index: number;
    end_index: number;
    url_citation?: {
      url: string;
      title: string;
    };
  }[];
}

export interface ImageData {
  id: string;
  type: "image";
  description: string;
  image_url: string;
  size: string;
  quality: string;
}


export type Data = TextData | ImageData

export interface OutputNode {
  id: string;
  title: string;
  description?: string;
  value: number;
  data?: Data;
  children: OutputNode[];
}


export interface OutputStore {
  output: OutputNode;
  addOutput: (parentId: string, parentTitle: string, newOutput: OutputNode) => void;
  addLeaf: (parentId: string, newLeaf: OutputNode) => void;
  removeLeaf: (id: string) => void;
  changeValue: (id: string, value: number) => void;
  addOrUpdateRootLeaf: (newLeaf: OutputNode) => void;
  reset: () => void;
}

export const useOutputStore = create<OutputStore>()(
  persist(
    immer(
      (set) => ({
        output: {
          id: "root",
          title: "root",
          value: 1,
          children: [],
        },
        addOutput: (parentId, parentTitle, newOutput) =>
          set((state) => {
            const parentOutput = state.output.children.find((child) => child.id === parentId);
            if(!parentOutput) {
              // If the parent output doesn't exist, create it and add the new output as its child
              state.output.children = [...state.output.children, { id: parentId, title: parentTitle, value: 1, children: [newOutput] }];
            } else {
              // If the parent output exists, add the new output as its child
              parentOutput.children = [...parentOutput.children, newOutput];
            }
          }),
        addLeaf: (parentId, newLeaf) =>
          set((state) => {
            const addLeafRecursively = (node: OutputNode): OutputNode => {
              if (node.id === parentId) {
                return { ...node, children: [...node.children, newLeaf] };
              }
              return {
                ...node,
                children: node.children.map(addLeafRecursively),
              };
            };

            state.output = addLeafRecursively(state.output);
          }),
        removeLeaf: (id) => {
          set((state) => {
            const removeLeafRecursively = (node: OutputNode): OutputNode => {
              if (node.id === id) {
                return { ...node, children: [] };
              }
              return {
                ...node,
                children: node.children
                  .map(removeLeafRecursively)
                  .filter((child) => child.id !== id),
              };
            };
            state.output = removeLeafRecursively(state.output);
          });
        },
        changeValue: (id, value) => {
          set((state) => {
            const changeValueRecursively = (node: OutputNode): OutputNode => {
              if (node.id === id) {
                return { ...node, value };
              }
              return {
                ...node,
                children: node.children.map(changeValueRecursively),
              };
            };
            state.output = changeValueRecursively(state.output);
          });
        },
        addOrUpdateRootLeaf: (newLeaf) => {
          set((state) => {
            const idx = state.output.children.findIndex((child) => child.id === newLeaf.id);
            //console.log("idx", idx, state.output.children, newLeaf);
            if (idx === -1) {
              state.output.children = [...state.output.children, newLeaf];
            } else {
              //newLeaf.children = state.output.children[idx].children;
              // Update the existing leaf with the new one (leaving children intact)
              state.output.children[idx] = {
                id: newLeaf.id,
                title: newLeaf.title,
                value: newLeaf.value,
                description: newLeaf.description,
                data: newLeaf.data,
                children: state.output.children[idx].children || [],
              };
            }
          });
        },
        reset: () => {
          set((state) => {
            state.output = {
              id: "root",
              title: "root",
              value: 1,
              children: [],
            };
          });
        },
      })
    ),
    {
      name: "output-storage",
      storage: createJSONStorage(() => localStorage),
    })
);