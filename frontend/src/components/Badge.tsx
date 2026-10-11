import type { Ton } from "../labels";

interface Props {
  ton: Ton;
  children: React.ReactNode;
}

export default function Badge({ ton, children }: Props) {
  const sinif = ton === "neutral" ? "badge" : `badge badge-${ton}`;
  return <span className={sinif}>{children}</span>;
}