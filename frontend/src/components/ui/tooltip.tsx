"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

// Simplified Tooltip for now
export const TooltipProvider = ({
  children,
}: {
  children: React.ReactNode;
}) => <>{children}</>;
export const Tooltip = ({ children }: { children: React.ReactNode }) => (
  <div className="relative group">{children}</div>
);
export const TooltipTrigger = ({ children, asChild }: any) => <>{children}</>;
export const TooltipContent = ({ children, className }: any) => (
  <div
    className={cn(
      "absolute hidden group-hover:block z-50 overflow-hidden rounded-md border bg-popover px-3 py-1.5 text-sm text-popover-foreground shadow-md animate-in fade-in-0 zoom-in-95",
      className
    )}
  >
    {children}
  </div>
);
