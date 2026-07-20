export interface Order {
  id: string;
  item: string;
  quantity: number;
  price: number;
  deletedAt: Date | null;
}

export const databaseCollection: Order[] = [];