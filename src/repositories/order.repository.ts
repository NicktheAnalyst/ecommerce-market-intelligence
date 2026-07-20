import { Order, databaseCollection } from '../models/order.model.ts';

export class OrderRepository {
  
  // 1. Optimized Bulk Inserts
  async bulkInsert(orders: Omit<Order, 'deletedAt'>[]): Promise<void> {
    const formattedOrders = orders.map(order => ({
      ...order,
      deletedAt: null
    }));
    databaseCollection.push(...formattedOrders);
    console.log(`Successfully bulk inserted ${orders.length} orders.`);
  }

  // 2. Implementing Soft Deletes (Fetch active only)
  async findActiveOrders(): Promise<Order[]> {
    return databaseCollection.filter((order: Order) => order.deletedAt === null);
  }

  // 2. Implementing Soft Deletes (Update timestamp)
  async softDelete(orderId: string): Promise<void> {
    const order = databaseCollection.find((o: Order) => o.id === orderId);
    if (order) {
      order.deletedAt = new Date();
    }
  }
}