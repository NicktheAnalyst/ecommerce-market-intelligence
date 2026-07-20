import express, { Request } from 'express';
import { idempotencyGuard } from './middleware/idempotency.middleware';
import { OrderRepository } from './repositories/order.repository';

const app = express();
app.use(express.json());

const orderRepo = new OrderRepository();

app.post('/orders/bulk', idempotencyGuard, async (req: Request, res: any) => {
  try {
    const ordersInput = req.body.orders;

    await orderRepo.bulkInsert(ordersInput);

    const successResponse = { status: 'success', message: 'Orders processed safely.' };

    if (res.saveToIdempotencyCache) {
      res.saveToIdempotencyCache(successResponse);
    }

    return res.status(201).json(successResponse);
  } catch (error) {
    return res.status(500).json({ error: 'Something went wrong' });
  }
});

app.listen(3000, () => console.log('Server running on port 3000'));