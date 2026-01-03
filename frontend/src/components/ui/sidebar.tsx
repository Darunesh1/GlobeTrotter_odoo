"use client";

import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva } from "class-variance-authority";
import { cn } from "@/lib/utils";
import { Sheet, SheetContent } from "@/components/ui/sheet";
import { Menu } from "lucide-react";

const SidebarContext = React.createContext<{
  state: "expanded" | "collapsed";
  openMobile: boolean;
  setOpenMobile: (open: boolean) => void;
  toggleSidebar: () => void;
}>({
  state: "expanded",
  openMobile: false,
  setOpenMobile: () => {},
  toggleSidebar: () => {},
});

export function SidebarProvider({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const [openMobile, setOpenMobile] = React.useState(false);
  return (
    <SidebarContext.Provider
      value={{
        state: "expanded",
        openMobile,
        setOpenMobile,
        toggleSidebar: () => {},
      }}
    >
      <div
        className={cn(
          "group/sidebar-wrapper flex min-h-svh w-full has-[[data-variant=inset]]:bg-sidebar",
          className
        )}
      >
        {children}
      </div>
    </SidebarContext.Provider>
  );
}

export function Sidebar({ children, collapsible }: any) {
  return (
    <>
      <div className="hidden md:flex flex-col w-[250px] bg-sidebar border-r border-sidebar-border text-sidebar-foreground">
        {children}
      </div>
      <Sheet>
        <SheetContent
          side="left"
          className="w-[260px] p-0 bg-sidebar text-sidebar-foreground"
        >
          {children}
        </SheetContent>
      </Sheet>
    </>
  );
}

export function SidebarTrigger({ className }: any) {
  return (
    <button className={className}>
      <Menu />
    </button>
  );
}

export function SidebarHeader({ children, className }: any) {
  return <div className={cn("p-4", className)}>{children}</div>;
}

export function SidebarContent({ children }: any) {
  return <div className="flex-1 overflow-auto">{children}</div>;
}

export function SidebarGroup({ children }: any) {
  return <div className="px-2 py-4">{children}</div>;
}

export function SidebarGroupLabel({ children }: any) {
  return (
    <div className="px-2 py-1 text-xs font-semibold text-muted-foreground uppercase">
      {children}
    </div>
  );
}

export function SidebarGroupContent({ children }: any) {
  return <div>{children}</div>;
}

export function SidebarMenu({ children }: any) {
  return <ul className="space-y-1">{children}</ul>;
}

export function SidebarMenuItem({ children }: any) {
  return <li>{children}</li>;
}

export function SidebarMenuButton({
  asChild,
  children,
  className,
  tooltip,
}: any) {
  const Comp = asChild ? Slot : "button";
  return (
    <Comp
      className={cn(
        "flex w-full items-center gap-2 rounded-md p-2 text-sm font-medium hover:bg-sidebar-accent hover:text-sidebar-accent-foreground",
        className
      )}
    >
      {children}
    </Comp>
  );
}

export function SidebarFooter({ children }: any) {
  return <div className="p-4 border-t border-sidebar-border">{children}</div>;
}

export function SidebarRail() {
  return null;
}
